import itertools
import re
import string
from dataclasses import dataclass, replace
from typing import (
    Any,
    Callable,
    Collection,
    Container,
    Dict,
    Iterable,
    List,
    Mapping,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from ...code_tools.code_builder import CodeBuilder
from ...code_tools.compiler import ClosureCompiler
from ...code_tools.utils import get_literal_expr
from ...model_tools.definitions import InputField, InputShape, OutputField, OutputShape
from ...provider.essential import Mediator, Request
from ...provider.request_cls import LocatedRequest, TypeHintLoc
from ...provider.static_provider import StaticProvider, static_provision_action
from .crown_definitions import (
    BaseCrown,
    BaseDictCrown,
    BaseFieldCrown,
    BaseListCrown,
    BaseNameLayout,
    BaseNoneCrown,
    BaseShape,
    ExtraCollect,
    ExtraTargets,
    InpCrown,
    InpDictCrown,
    InpExtraMove,
    InpFieldCrown,
    InpListCrown,
    InpNoneCrown,
    OutExtraMove,
)


@dataclass
class CodeGenHookData:
    namespace: Dict[str, Any]
    source: str


CodeGenHook = Callable[[CodeGenHookData], None]


def stub_code_gen_hook(data: CodeGenHookData):
    pass


@dataclass(frozen=True)
class CodeGenHookRequest(Request[CodeGenHook]):
    pass


class CodeGenAccumulator(StaticProvider):
    """Accumulates all generated code. It may be useful for debugging"""

    def __init__(self) -> None:
        self.list: List[Tuple[Sequence[Request], CodeGenHookData]] = []

    @static_provision_action
    def _provide_code_gen_hook(self, mediator: Mediator, request: CodeGenHookRequest) -> CodeGenHook:
        request_stack = mediator.request_stack

        def hook(data: CodeGenHookData):
            self.list.append((request_stack, data))

        return hook

    @property
    def code_pairs(self):
        return [
            (request_stack[-2].loc_map[TypeHintLoc].type, hook_data.source)
            for request_stack, hook_data in self.list
            if (
                len(request_stack) >= 2
                and isinstance(request_stack[-2], LocatedRequest)
                and request_stack[-2].loc_map.has(TypeHintLoc)
                and request_stack[-2].loc_map[TypeHintLoc].type
            )
        ]

    @property
    def code_dict(self):
        return dict(self.code_pairs)


T = TypeVar('T')


def _concatenate_iters(args: Iterable[Iterable[T]]) -> Collection[T]:
    return list(itertools.chain.from_iterable(args))


def _inner_collect_used_direct_fields(crown: BaseCrown) -> Iterable[str]:
    if isinstance(crown, BaseDictCrown):
        return _concatenate_iters(
            _inner_collect_used_direct_fields(sub_crown)
            for sub_crown in crown.map.values()
        )
    if isinstance(crown, BaseListCrown):
        return _concatenate_iters(
            _inner_collect_used_direct_fields(sub_crown)
            for sub_crown in crown.map
        )
    if isinstance(crown, BaseFieldCrown):
        return [crown.id]
    if isinstance(crown, BaseNoneCrown):
        return []
    raise TypeError


def _collect_used_direct_fields(crown: BaseCrown) -> Set[str]:
    lst = _inner_collect_used_direct_fields(crown)

    used_set = set()
    for f_name in lst:
        if f_name in used_set:
            raise ValueError(f"Field {f_name!r} is duplicated at crown")
        used_set.add(f_name)

    return used_set


def get_skipped_fields(shape: BaseShape, name_layout: BaseNameLayout) -> Collection[str]:
    used_direct_fields = _collect_used_direct_fields(name_layout.crown)
    if isinstance(name_layout.extra_move, ExtraTargets):
        extra_targets = name_layout.extra_move.fields
    else:
        extra_targets = ()

    return [
        field.id for field in shape.fields
        if field.id not in used_direct_fields and field.id not in extra_targets
    ]


def _inner_get_extra_targets_at_crown(extra_targets: Container[str], crown: BaseCrown) -> Collection[str]:
    if isinstance(crown, BaseDictCrown):
        return _concatenate_iters(
            _inner_get_extra_targets_at_crown(extra_targets, sub_crown)
            for sub_crown in crown.map.values()
        )
    if isinstance(crown, BaseListCrown):
        return _concatenate_iters(
            _inner_get_extra_targets_at_crown(extra_targets, sub_crown)
            for sub_crown in crown.map
        )
    if isinstance(crown, BaseFieldCrown):
        return [crown.id] if crown.id in extra_targets else []
    if isinstance(crown, BaseNoneCrown):
        return []
    raise TypeError


def get_extra_targets_at_crown(name_layout: BaseNameLayout) -> Collection[str]:
    if not isinstance(name_layout.extra_move, ExtraTargets):
        return []

    return _inner_get_extra_targets_at_crown(name_layout.extra_move.fields, name_layout.crown)


def get_optional_fields_at_list_crown(
    fields_map: Mapping[str, Union[InputField, OutputField]],
    crown: BaseCrown,
) -> Collection[str]:
    if isinstance(crown, BaseDictCrown):
        return _concatenate_iters(
            get_optional_fields_at_list_crown(fields_map, sub_crown)
            for sub_crown in crown.map.values()
        )
    if isinstance(crown, BaseListCrown):
        return _concatenate_iters(
            (
                [sub_crown.id]
                if fields_map[sub_crown.id].is_optional else
                []
            )
            if isinstance(sub_crown, BaseFieldCrown) else
            get_optional_fields_at_list_crown(fields_map, sub_crown)
            for sub_crown in crown.map
        )
    if isinstance(crown, (BaseFieldCrown, BaseNoneCrown)):
        return []
    raise TypeError


def get_wild_extra_targets(shape: BaseShape, extra_move: Union[InpExtraMove, OutExtraMove]) -> Collection[str]:
    if not isinstance(extra_move, ExtraTargets):
        return []

    return [
        target for target in extra_move.fields
        if target not in shape.fields_dict.keys()
    ]


def strip_input_shape_fields(shape: InputShape, skipped_fields: Collection[str]) -> InputShape:
    skipped_required_fields = [
        field.id
        for field in shape.fields
        if field.is_required and field.id in skipped_fields
    ]
    if skipped_required_fields:
        raise ValueError(
            f"Required fields {skipped_required_fields} are skipped"
        )
    return replace(
        shape,
        fields=tuple(
            field for field in shape.fields
            if field.id not in skipped_fields
        ),
        params=tuple(
            param for param in shape.params
            if param.field_id not in skipped_fields
        ),
        overriden_types=frozenset(
            field.id for field in shape.fields
            if field.id not in skipped_fields
        ),
    )


def strip_output_shape_fields(shape: OutputShape, skipped_fields: Collection[str]) -> OutputShape:
    return replace(
        shape,
        fields=tuple(
            field for field in shape.fields
            if field.id not in skipped_fields
        ),
        overriden_types=frozenset(
            field.id for field in shape.fields
            if field.id not in skipped_fields
        )
    )


class NameSanitizer:
    _BAD_CHARS = re.compile(r'\W')
    _TRANSLATE_MAP = str.maketrans({'.': '_', '[': '_'})

    def sanitize(self, name: str) -> str:
        if name == "":
            return ""

        first_letter = name[0] if name[0] in string.ascii_letters else '_'
        return first_letter + self._BAD_CHARS.sub('', name[1:].translate(self._TRANSLATE_MAP))


def compile_closure_with_globals_capturing(
    compiler: ClosureCompiler,
    code_gen_hook: CodeGenHook,
    namespace: Dict[str, object],
    body_builders: Iterable[CodeBuilder],
    *,
    closure_name: str,
    closure_params: str,
    file_name: str,
):
    builder = CodeBuilder()

    global_namespace_dict = {}
    for name, value in namespace.items():
        value_literal = get_literal_expr(value)
        if value_literal is None:
            global_name = f"g_{name}"
            global_namespace_dict[global_name] = value
            builder += f"{name} = {global_name}"
        else:
            builder += f"{name} = {value_literal}"

    builder.empty_line()

    with builder(f"def {closure_name}({closure_params}):"):
        for body_builder in body_builders:
            builder.extend(body_builder)

    builder += f"return {closure_name}"

    code_gen_hook(
        CodeGenHookData(
            namespace=global_namespace_dict,
            source=builder.string(),
        )
    )

    return compiler.compile(
        file_name,
        lambda uid: f'<adaptix generated {uid}>',
        builder,
        global_namespace_dict,
    )


def has_collect_policy(crown: InpCrown) -> bool:
    if isinstance(crown, InpDictCrown):
        return crown.extra_policy == ExtraCollect() or any(
            has_collect_policy(sub_crown)
            for sub_crown in crown.map.values()
        )
    if isinstance(crown, InpListCrown):
        return any(
            has_collect_policy(sub_crown)
            for sub_crown in crown.map
        )
    if isinstance(crown, (InpFieldCrown, InpNoneCrown)):
        return False
    raise TypeError

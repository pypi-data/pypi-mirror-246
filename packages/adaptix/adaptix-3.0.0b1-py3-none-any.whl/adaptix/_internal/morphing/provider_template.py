from abc import ABC, abstractmethod
from typing import final

from ..common import Dumper, Loader, TypeHint
from ..provider.essential import CannotProvide, Mediator
from ..provider.provider_template import ProviderWithAttachableRC
from ..provider.request_cls import DumperRequest, LoaderRequest, LocMap, TypeHintLoc
from ..provider.request_filtering import ExactOriginRC
from ..provider.static_provider import static_provision_action
from ..type_tools import normalize_type


class LoaderProvider(ProviderWithAttachableRC, ABC):
    @final
    @static_provision_action
    def _outer_provide_loader(self, mediator: Mediator, request: LoaderRequest):
        self._request_checker.check_request(mediator, request)
        return self._provide_loader(mediator, request)

    @abstractmethod
    def _provide_loader(self, mediator: Mediator, request: LoaderRequest) -> Loader:
        ...


class DumperProvider(ProviderWithAttachableRC, ABC):
    @final
    @static_provision_action
    def _outer_provide_dumper(self, mediator: Mediator, request: DumperRequest):
        self._request_checker.check_request(mediator, request)
        return self._provide_dumper(mediator, request)

    @abstractmethod
    def _provide_dumper(self, mediator: Mediator, request: DumperRequest) -> Dumper:
        ...


class ABCProxy(LoaderProvider, DumperProvider):
    def __init__(self, abstract: TypeHint, impl: TypeHint, for_loader: bool = True, for_dumper: bool = True):
        self._abstract = normalize_type(abstract).origin
        self._impl = impl
        self._request_checker = ExactOriginRC(self._abstract)
        self._for_loader = for_loader
        self._for_dumper = for_dumper

    def _provide_loader(self, mediator: Mediator, request: LoaderRequest) -> Loader:
        if not self._for_loader:
            raise CannotProvide

        return mediator.mandatory_provide(
            LoaderRequest(
                loc_map=LocMap(TypeHintLoc(type=self._impl))
            ),
            lambda x: f'Cannot create loader for union. Loader for {self._impl} cannot be created',
        )

    def _provide_dumper(self, mediator: Mediator, request: DumperRequest) -> Dumper:
        if not self._for_dumper:
            raise CannotProvide

        return mediator.mandatory_provide(
            DumperRequest(
                loc_map=LocMap(TypeHintLoc(type=self._impl))
            ),
            lambda x: f'Cannot create dumper for union. Dumper for {self._impl} cannot be created',
        )

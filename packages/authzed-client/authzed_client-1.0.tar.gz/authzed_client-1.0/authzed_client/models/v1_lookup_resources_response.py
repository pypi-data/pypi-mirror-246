from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.lookup_permissionship_represents_whether_a_lookup_response_was_partially_evaluated_or_not import (
    LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat import (
        PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat,
    )
    from ..models.v1_cursor import V1Cursor
    from ..models.v1_zed_token import V1ZedToken


T = TypeVar("T", bound="V1LookupResourcesResponse")


@_attrs_define
class V1LookupResourcesResponse:
    """LookupResourcesResponse contains a single matching resource object ID for the
    requested object type, permission, and subject.

        Attributes:
            looked_up_at (Union[Unset, V1ZedToken]): ZedToken is used to provide causality metadata between Write and Check
                requests.

                See the authzed.api.v1.Consistency message for more information.
            resource_object_id (Union[Unset, str]): resource_object_id is the object ID of the found resource.
            permissionship (Union[Unset, LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot]):
                Default: LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot.LOOKUP_PERMISSIONSHIP_UN
                SPECIFIED.
            partial_caveat_info (Union[Unset, PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEvent
                AResponseContainsAPartiallyEvaluatedCaveat]):
            after_result_cursor (Union[Unset, V1Cursor]): Cursor is used to provide resumption of listing between calls to
                APIs
                such as LookupResources.
    """

    looked_up_at: Union[Unset, "V1ZedToken"] = UNSET
    resource_object_id: Union[Unset, str] = UNSET
    permissionship: Union[
        Unset, LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot
    ] = LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot.LOOKUP_PERMISSIONSHIP_UNSPECIFIED
    partial_caveat_info: Union[
        Unset,
        "PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat",
    ] = UNSET
    after_result_cursor: Union[Unset, "V1Cursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        looked_up_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.looked_up_at, Unset):
            looked_up_at = self.looked_up_at.to_dict()

        resource_object_id = self.resource_object_id
        permissionship: Union[Unset, str] = UNSET
        if not isinstance(self.permissionship, Unset):
            permissionship = self.permissionship.value

        partial_caveat_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partial_caveat_info, Unset):
            partial_caveat_info = self.partial_caveat_info.to_dict()

        after_result_cursor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.after_result_cursor, Unset):
            after_result_cursor = self.after_result_cursor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if looked_up_at is not UNSET:
            field_dict["lookedUpAt"] = looked_up_at
        if resource_object_id is not UNSET:
            field_dict["resourceObjectId"] = resource_object_id
        if permissionship is not UNSET:
            field_dict["permissionship"] = permissionship
        if partial_caveat_info is not UNSET:
            field_dict["partialCaveatInfo"] = partial_caveat_info
        if after_result_cursor is not UNSET:
            field_dict["afterResultCursor"] = after_result_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat import (
            PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat,
        )
        from ..models.v1_cursor import V1Cursor
        from ..models.v1_zed_token import V1ZedToken

        d = src_dict.copy()
        _looked_up_at = d.pop("lookedUpAt", UNSET)
        looked_up_at: Union[Unset, V1ZedToken]
        if isinstance(_looked_up_at, Unset):
            looked_up_at = UNSET
        else:
            looked_up_at = V1ZedToken.from_dict(_looked_up_at)

        resource_object_id = d.pop("resourceObjectId", UNSET)

        _permissionship = d.pop("permissionship", UNSET)
        permissionship: Union[Unset, LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot]
        if isinstance(_permissionship, Unset):
            permissionship = UNSET
        else:
            permissionship = LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot(
                _permissionship
            )

        _partial_caveat_info = d.pop("partialCaveatInfo", UNSET)
        partial_caveat_info: Union[
            Unset,
            PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat,
        ]
        if isinstance(_partial_caveat_info, Unset):
            partial_caveat_info = UNSET
        else:
            partial_caveat_info = PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat.from_dict(
                _partial_caveat_info
            )

        _after_result_cursor = d.pop("afterResultCursor", UNSET)
        after_result_cursor: Union[Unset, V1Cursor]
        if isinstance(_after_result_cursor, Unset):
            after_result_cursor = UNSET
        else:
            after_result_cursor = V1Cursor.from_dict(_after_result_cursor)

        v1_lookup_resources_response = cls(
            looked_up_at=looked_up_at,
            resource_object_id=resource_object_id,
            permissionship=permissionship,
            partial_caveat_info=partial_caveat_info,
            after_result_cursor=after_result_cursor,
        )

        v1_lookup_resources_response.additional_properties = d
        return v1_lookup_resources_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

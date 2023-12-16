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


T = TypeVar("T", bound="V1ResolvedSubject")


@_attrs_define
class V1ResolvedSubject:
    """ResolvedSubject is a single subject resolved within LookupSubjects.

    Attributes:
        subject_object_id (Union[Unset, str]): subject_object_id is the Object ID of the subject found. May be a `*` if
            a wildcard was found.
        permissionship (Union[Unset, LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot]):
            Default: LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot.LOOKUP_PERMISSIONSHIP_UN
            SPECIFIED.
        partial_caveat_info (Union[Unset, PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEvent
            AResponseContainsAPartiallyEvaluatedCaveat]):
    """

    subject_object_id: Union[Unset, str] = UNSET
    permissionship: Union[
        Unset, LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot
    ] = LookupPermissionshipRepresentsWhetherALookupResponseWasPartiallyEvaluatedOrNot.LOOKUP_PERMISSIONSHIP_UNSPECIFIED
    partial_caveat_info: Union[
        Unset,
        "PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat",
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_object_id = self.subject_object_id
        permissionship: Union[Unset, str] = UNSET
        if not isinstance(self.permissionship, Unset):
            permissionship = self.permissionship.value

        partial_caveat_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partial_caveat_info, Unset):
            partial_caveat_info = self.partial_caveat_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subject_object_id is not UNSET:
            field_dict["subjectObjectId"] = subject_object_id
        if permissionship is not UNSET:
            field_dict["permissionship"] = permissionship
        if partial_caveat_info is not UNSET:
            field_dict["partialCaveatInfo"] = partial_caveat_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat import (
            PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat,
        )

        d = src_dict.copy()
        subject_object_id = d.pop("subjectObjectId", UNSET)

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

        v1_resolved_subject = cls(
            subject_object_id=subject_object_id,
            permissionship=permissionship,
            partial_caveat_info=partial_caveat_info,
        )

        v1_resolved_subject.additional_properties = d
        return v1_resolved_subject

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

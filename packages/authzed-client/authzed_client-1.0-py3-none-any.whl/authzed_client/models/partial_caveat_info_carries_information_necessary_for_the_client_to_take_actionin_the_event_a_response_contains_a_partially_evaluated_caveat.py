from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar(
    "T",
    bound="PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat",
)


@_attrs_define
class PartialCaveatInfoCarriesInformationNecessaryForTheClientToTakeActioninTheEventAResponseContainsAPartiallyEvaluatedCaveat:
    """
    Attributes:
        missing_required_context (Union[Unset, List[str]]):
    """

    missing_required_context: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        missing_required_context: Union[Unset, List[str]] = UNSET
        if not isinstance(self.missing_required_context, Unset):
            missing_required_context = self.missing_required_context

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if missing_required_context is not UNSET:
            field_dict["missingRequiredContext"] = missing_required_context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        missing_required_context = cast(List[str], d.pop("missingRequiredContext", UNSET))

        partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat = cls(
            missing_required_context=missing_required_context,
        )

        partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat.additional_properties = d
        return partial_caveat_info_carries_information_necessary_for_the_client_to_take_actionin_the_event_a_response_contains_a_partially_evaluated_caveat

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

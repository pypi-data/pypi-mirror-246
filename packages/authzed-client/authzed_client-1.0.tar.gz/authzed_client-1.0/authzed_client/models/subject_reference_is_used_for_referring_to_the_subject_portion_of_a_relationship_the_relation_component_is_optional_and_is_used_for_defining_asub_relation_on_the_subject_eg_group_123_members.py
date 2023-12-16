from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_object_reference import V1ObjectReference


T = TypeVar(
    "T",
    bound="SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members",
)


@_attrs_define
class SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members:
    """
    Attributes:
        object_ (Union[Unset, V1ObjectReference]): ObjectReference is used to refer to a specific object in the system.
        optional_relation (Union[Unset, str]):
    """

    object_: Union[Unset, "V1ObjectReference"] = UNSET
    optional_relation: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()

        optional_relation = self.optional_relation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if optional_relation is not UNSET:
            field_dict["optionalRelation"] = optional_relation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_object_reference import V1ObjectReference

        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, V1ObjectReference]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = V1ObjectReference.from_dict(_object_)

        optional_relation = d.pop("optionalRelation", UNSET)

        subject_reference_is_used_for_referring_to_the_subject_portion_of_a_relationship_the_relation_component_is_optional_and_is_used_for_defining_asub_relation_on_the_subject_eg_group_123_members = cls(
            object_=object_,
            optional_relation=optional_relation,
        )

        subject_reference_is_used_for_referring_to_the_subject_portion_of_a_relationship_the_relation_component_is_optional_and_is_used_for_defining_asub_relation_on_the_subject_eg_group_123_members.additional_properties = d
        return subject_reference_is_used_for_referring_to_the_subject_portion_of_a_relationship_the_relation_component_is_optional_and_is_used_for_defining_asub_relation_on_the_subject_eg_group_123_members

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subject_reference_is_used_for_referring_to_the_subject_portion_of_a_relationship_the_relation_component_is_optional_and_is_used_for_defining_asub_relation_on_the_subject_eg_group_123_members import (
        SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members,
    )


T = TypeVar("T", bound="V1DirectSubjectSet")


@_attrs_define
class V1DirectSubjectSet:
    """DirectSubjectSet is a subject set which is simply a collection of subjects.

    Attributes:
        subjects (Union[Unset, List['SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComp
            onentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members']]):
    """

    subjects: Union[
        Unset,
        List[
            "SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members"
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subjects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subjects, Unset):
            subjects = []
            for subjects_item_data in self.subjects:
                subjects_item = subjects_item_data.to_dict()

                subjects.append(subjects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subjects is not UNSET:
            field_dict["subjects"] = subjects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subject_reference_is_used_for_referring_to_the_subject_portion_of_a_relationship_the_relation_component_is_optional_and_is_used_for_defining_asub_relation_on_the_subject_eg_group_123_members import (
            SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members,
        )

        d = src_dict.copy()
        subjects = []
        _subjects = d.pop("subjects", UNSET)
        for subjects_item_data in _subjects or []:
            subjects_item = SubjectReferenceIsUsedForReferringToTheSubjectPortionOfARelationshipTheRelationComponentIsOptionalAndIsUsedForDefiningAsubRelationOnTheSubjectEGGroup123Members.from_dict(
                subjects_item_data
            )

            subjects.append(subjects_item)

        v1_direct_subject_set = cls(
            subjects=subjects,
        )

        v1_direct_subject_set.additional_properties = d
        return v1_direct_subject_set

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

import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.s_type_enum import STypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Scanner")


@_attrs_define
class Scanner:
    """
    Attributes:
        id (int):
        s_type (STypeEnum): * `0` - k8s
            * `1` - enumerator
            * `2` - httpx
            * `3` - nuclei
        name (str):
        enabled (bool):
        config (Union[Unset, None, str]):
        comment (Union[Unset, None, str]):
        created_at (Optional[datetime.datetime]):
        updated_at (Optional[datetime.datetime]):
        version (Union[Unset, None, str]):
        commit (Union[Unset, None, str]):
    """

    id: int
    s_type: STypeEnum
    name: str
    enabled: bool
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    config: Union[Unset, None, str] = UNSET
    comment: Union[Unset, None, str] = UNSET
    version: Union[Unset, None, str] = UNSET
    commit: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        s_type = self.s_type.value

        name = self.name
        enabled = self.enabled
        config = self.config
        comment = self.comment
        created_at = self.created_at.isoformat() if self.created_at else None

        updated_at = self.updated_at.isoformat() if self.updated_at else None

        version = self.version
        commit = self.commit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "s_type": s_type,
                "name": name,
                "enabled": enabled,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if config is not UNSET:
            field_dict["config"] = config
        if comment is not UNSET:
            field_dict["comment"] = comment
        if version is not UNSET:
            field_dict["version"] = version
        if commit is not UNSET:
            field_dict["commit"] = commit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        s_type = STypeEnum(d.pop("s_type"))

        name = d.pop("name")

        enabled = d.pop("enabled")

        config = d.pop("config", UNSET)

        comment = d.pop("comment", UNSET)

        _created_at = d.pop("created_at")
        created_at: Optional[datetime.datetime]
        if _created_at is None:
            created_at = None
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at")
        updated_at: Optional[datetime.datetime]
        if _updated_at is None:
            updated_at = None
        else:
            updated_at = isoparse(_updated_at)

        version = d.pop("version", UNSET)

        commit = d.pop("commit", UNSET)

        scanner = cls(
            id=id,
            s_type=s_type,
            name=name,
            enabled=enabled,
            config=config,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            commit=commit,
        )

        scanner.additional_properties = d
        return scanner

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

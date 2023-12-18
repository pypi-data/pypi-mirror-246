from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Boto3ConnectionSettingsV2Response200")


@_attrs_define
class Boto3ConnectionSettingsV2Response200:
    """
    Attributes:
        endpoint_url (str):
        region_name (str):
        use_ssl (bool):
        aws_access_key_id (Union[Unset, str]):
        aws_secret_access_key (Union[Unset, str]):
    """

    endpoint_url: str
    region_name: str
    use_ssl: bool
    aws_access_key_id: Union[Unset, str] = UNSET
    aws_secret_access_key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        endpoint_url = self.endpoint_url
        region_name = self.region_name
        use_ssl = self.use_ssl
        aws_access_key_id = self.aws_access_key_id
        aws_secret_access_key = self.aws_secret_access_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endpoint_url": endpoint_url,
                "region_name": region_name,
                "use_ssl": use_ssl,
            }
        )
        if aws_access_key_id is not UNSET:
            field_dict["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key is not UNSET:
            field_dict["aws_secret_access_key"] = aws_secret_access_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        endpoint_url = d.pop("endpoint_url")

        region_name = d.pop("region_name")

        use_ssl = d.pop("use_ssl")

        aws_access_key_id = d.pop("aws_access_key_id", UNSET)

        aws_secret_access_key = d.pop("aws_secret_access_key", UNSET)

        boto_3_connection_settings_v2_response_200 = cls(
            endpoint_url=endpoint_url,
            region_name=region_name,
            use_ssl=use_ssl,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        boto_3_connection_settings_v2_response_200.additional_properties = d
        return boto_3_connection_settings_v2_response_200

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

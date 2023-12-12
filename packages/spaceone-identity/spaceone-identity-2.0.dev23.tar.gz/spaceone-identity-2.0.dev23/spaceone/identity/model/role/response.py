from datetime import datetime
from typing import Union, List
from pydantic import BaseModel
from spaceone.core import utils

from spaceone.identity.model.role.request import RoleType, PagePermission

__all__ = ["RoleResponse", "RolesResponse"]


class RoleResponse(BaseModel):
    role_id: Union[str, None] = None
    name: Union[str, None] = None
    role_type: Union[RoleType, None] = None
    api_permissions: Union[List[str], None] = None
    page_permissions: Union[List[PagePermission], None] = None
    tags: Union[dict, None] = None
    is_managed: Union[bool, None] = None
    domain_id: Union[str, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data['created_at'] = utils.datetime_to_iso8601(data['created_at'])
        data['updated_at'] = utils.datetime_to_iso8601(data['updated_at'])
        return data


class RolesResponse(BaseModel):
    results: List[RoleResponse]
    total_count: int

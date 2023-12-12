from typing import Union, Literal, List
from pydantic import BaseModel

__all__ = [
    "UserSearchQueryRequest",
    "UserCreateRequest",
    "UserUpdateRequest",
    "UserVerifyEmailRequest",
    "UserStatQueryRequest",
    "UserConfirmEmailRequest",
    "UserResetPasswordRequest",
    "UserSetRequiredActionsRequest",
    "UserEnableMFARequest",
    "UserDisableMFARequest",
    "UserConfirmMFARequest",
    "UserDeleteRequest",
    "UserEnableRequest",
    "UserDisableRequest",
    "UserGetRequest",
    "UserFindRequest",
    "UserWorkspacesRequest",
    "AuthType",
    "State",
]

State = Literal["ENABLED", "DISABLED", "PENDING"]
AuthType = Literal["LOCAL", "EXTERNAL"]
PermissionGroup = Literal["DOMAIN", "WORKSPACE"]


class UserCreateRequest(BaseModel):
    user_id: str
    password: Union[str, None] = None
    name: Union[str, None] = ""
    email: Union[str, None] = ""
    auth_type: AuthType
    language: Union[str, None] = None
    timezone: Union[str, None] = None
    tags: Union[dict, None] = None
    reset_password: Union[bool, None] = False
    domain_id: str


class UserUpdateRequest(BaseModel):
    user_id: str
    password: Union[str, None] = None
    name: Union[str, None] = None
    email: Union[str, None] = None
    language: Union[str, None] = None
    timezone: Union[str, None] = None
    tags: Union[dict, None] = None
    reset_password: Union[bool, None] = None
    domain_id: str


class UserVerifyEmailRequest(BaseModel):
    user_id: str
    email: Union[str, None] = None
    force: Union[bool, None] = None
    domain_id: str


class UserConfirmEmailRequest(BaseModel):
    user_id: str
    verify_code: str
    domain_id: str


class UserResetPasswordRequest(BaseModel):
    user_id: str
    domain_id: str


class UserSetRequiredActionsRequest(BaseModel):
    user_id: str
    actions: List[str]
    domain_id: str


class UserEnableMFARequest(BaseModel):
    user_id: str
    mfa_type: str
    options: dict
    domain_id: str


class UserDisableMFARequest(BaseModel):
    user_id: str
    force: Union[bool, None] = None
    domain_id: str


class UserConfirmMFARequest(BaseModel):
    user_id: str
    verify_code: str
    domain_id: str


class UserDeleteRequest(BaseModel):
    user_id: str
    domain_id: str


class UserEnableRequest(BaseModel):
    user_id: str
    domain_id: str


class UserDisableRequest(BaseModel):
    user_id: str
    domain_id: str


class UserGetRequest(BaseModel):
    user_id: str
    domain_id: str


class UserWorkspacesRequest(BaseModel):
    user_id: str
    domain_id: str


class UserFindRequest(BaseModel):
    keyword: Union[str, None] = None
    state: Union[State, None] = None
    exclude_workspace_id: Union[str, None] = None
    page: Union[dict, None] = None
    domain_id: str


class UserSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    user_id: Union[str, None] = None
    name: Union[str, None] = None
    state: Union[State, None] = None
    email: Union[str, None] = None
    auth_type: Union[AuthType, None] = None
    domain_id: str


class UserStatQueryRequest(BaseModel):
    query: dict
    domain_id: str

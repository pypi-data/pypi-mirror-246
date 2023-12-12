import logging
import time
import random
from abc import abstractmethod, ABC, ABCMeta

from spaceone.core import config, utils, cache
from spaceone.core.manager import BaseManager
from spaceone.core.auth.jwt.jwt_util import JWTUtil

from spaceone.identity.lib.key_generator import KeyGenerator
from spaceone.identity.error.error_token import *
from spaceone.identity.error.error_authentication import *

__all__ = ["TokenManager", "JWTManager"]
_LOGGER = logging.getLogger(__name__)


class TokenManager(BaseManager, ABC):
    is_authenticated = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_conf()

    @abstractmethod
    def issue_temporary_token(self, **kwargs):
        pass

    @abstractmethod
    def issue_token(self, **kwargs):
        pass

    @abstractmethod
    def refresh_token(self, user_id, domain_id, **kwargs):
        pass

    @abstractmethod
    def authenticate(self, user_id, domain_id, credentials):
        pass

    @abstractmethod
    def check_refreshable(self, key, ttl):
        pass

    def _load_conf(self):
        identity_conf = config.get_global("IDENTITY") or {}
        token_conf = identity_conf.get("token", {})
        self.CONST_TOKEN_TIMEOUT = token_conf.get("token_timeout", 1800)
        self.CONST_VERIFY_CODE_TIMEOUT = token_conf.get("verify_code_timeout", 3600)
        self.CONST_REFRESH_TIMEOUT = token_conf.get("refresh_timeout", 3600)
        self.CONST_REFRESH_TTL = token_conf.get("refresh_ttl", -1)
        self.CONST_REFRESH_ONCE = token_conf.get("refresh_once", True)


class JWTManager(TokenManager, metaclass=ABCMeta):
    auth_type = None
    user = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_refresh_key = None

    def issue_temporary_token(self, **kwargs):
        raise NotImplementedError("TokenManager.issue_temporary_token not implemented!")

    def issue_token(self, **kwargs):
        raise NotImplementedError("TokenManager.issue_token not implemented!")

    def refresh_token(self, user_id, domain_id, **kwargs):
        raise NotImplementedError("TokenManager.refresh_token not implemented!")

    def authenticate(self, user_id, domain_id, credentials):
        raise NotImplementedError("TokenManager.authenticate not implemented!")

    def check_refreshable(self, refresh_key, ttl):
        if self.CONST_REFRESH_ONCE:
            if (
                cache.is_set()
                and cache.get(f"identity:refresh-token:{refresh_key}") is None
            ):
                raise ERROR_INVALID_REFRESH_TOKEN()

        if ttl == 0:
            raise ERROR_REFRESH_COUNT()

        self.is_authenticated = True
        self.old_refresh_key = refresh_key

    def issue_access_token(self, user_id, domain_id, **kwargs):
        private_jwk = self._get_private_jwk(kwargs)
        permissions = kwargs.get("permissions")
        timeout = kwargs.get("timeout")
        if timeout is None:
            timeout = self.CONST_TOKEN_TIMEOUT

        payload = {
            "cat": "ACCESS_TOKEN",  # ACCESS_TOKEN | API_KEY
            # "token_type": "USER",  # USER | APP
            "did": domain_id,
            "aud": user_id,
            "iat": int(time.time()),
            "exp": int(time.time() + timeout),
        }

        if permissions:
            payload["permissions"] = permissions

        encoded = JWTUtil.encode(payload, private_jwk)
        return encoded

    def issue_refresh_token(self, user_type, user_id, domain_id, **kwargs):
        refresh_private_jwk = self._get_refresh_private_jwk(kwargs)
        ttl = kwargs.get("ttl")
        timeout = kwargs.get("timeout")

        if ttl is None:
            ttl = self.CONST_REFRESH_TTL
        elif ttl > self.CONST_REFRESH_TTL:
            raise ERROR_MAX_REFRESH_COUNT(max_refresh_count=self.CONST_REFRESH_TTL)

        if timeout is None:
            timeout = self.CONST_REFRESH_TIMEOUT

        refresh_key = self._generate_refresh_key()

        payload = {
            "cat": "REFRESH_TOKEN",
            "user_type": user_type,
            "did": domain_id,
            "aud": user_id,
            "iat": int(time.time()),
            "exp": int(time.time() + timeout),
            "key": refresh_key,
            "ttl": ttl,
        }

        encoded = JWTUtil.encode(payload, refresh_private_jwk)

        if self.CONST_REFRESH_ONCE:
            self._set_refresh_token_cache(refresh_key)

        return encoded

    @staticmethod
    def _generate_refresh_key():
        return utils.random_string(16)

    @staticmethod
    def _get_private_jwk(kwargs):
        if "private_jwk" not in kwargs:
            raise ERROR_NOT_FOUND_PRIVATE_KEY(purpose="Access Token")

        return kwargs["private_jwk"]

    @staticmethod
    def _get_refresh_private_jwk(kwargs):
        if "refresh_private_jwk" not in kwargs:
            raise ERROR_NOT_FOUND_PRIVATE_KEY(purpose="Refresh Token")

        return kwargs["refresh_private_jwk"]

    def _set_refresh_token_cache(self, new_refresh_key):
        if cache.is_set():
            if self.old_refresh_key:
                cache.delete(f"identity:refresh-token:{self.old_refresh_key}")

            cache.set(
                f"identity:refresh-token:{new_refresh_key}",
                "",
                expire=self.CONST_REFRESH_TIMEOUT,
            )

    def create_verify_code(self, user_id, domain_id):
        if cache.is_set():
            verify_code = self._generate_verify_code()
            cache.delete(f"verify-code:{domain_id}:{user_id}")
            cache.set(
                f"verify-code:{domain_id}:{user_id}",
                verify_code,
                expire=self.CONST_VERIFY_CODE_TIMEOUT,
            )
            return verify_code

    @staticmethod
    def check_verify_code(user_id, domain_id, verify_code):
        if cache.is_set():
            cached_verify_code = cache.get(f"verify-code:{domain_id}:{user_id}")
            if cached_verify_code == verify_code:
                return True
        return False

    @staticmethod
    def _generate_verify_code():
        return str(random.randint(100000, 999999))

    @classmethod
    def get_token_manager_by_auth_type(cls, auth_type):
        for subclass in cls.__subclasses__():
            if subclass.auth_type == auth_type:
                return subclass()
        raise ERROR_INVALID_AUTHENTICATION_TYPE(auth_type=auth_type)

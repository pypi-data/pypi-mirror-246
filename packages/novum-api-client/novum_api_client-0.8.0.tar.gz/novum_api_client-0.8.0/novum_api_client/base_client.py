# pylint: disable=C0103
# pylint: disable=C0115
# pylint: disable=C0116
# flake8: noqa

from dataclasses import asdict, dataclass
import json
import time
import base64
import hashlib
from datetime import datetime
from urllib.parse import unquote
from threading import Timer
from typing import List, Optional, Any
import requests
from .api_type import TChargeTypes, TUser, TUserEssentials

TOKEN_REFRESH_INTERVAL_SCALE = 0.9
PRODUCTION_API_HOST: str = "https://novum-batteries.com"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        if isinstance(o, TChargeTypes):
            return o.value
        return super().default(o)


class NovumAPIError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


def get_sha_256(to_hash: str) -> str:
    to_hash_bytes = to_hash.encode("utf-8")
    sha256_hash = hashlib.sha256(to_hash_bytes)
    return sha256_hash.hexdigest()


def user_name(user: TUserEssentials) -> str:
    if user.profile is not None and user.profile.name is not None:
        return str(user.profile.name)
    else:
        raise ValueError("No user defined.")


def full_name(user: TUser) -> str:
    if (
        user.profile is not None
        and user.profile.first_name is not None
        and user.profile.family_name is not None
    ):
        return str(user.profile.first_name) + " " + str(user.profile.family_name)
    else:
        raise ValueError("No user name defined.")


def parse_jwt(token: str) -> dict:
    base64_input = token.split(".")[1]
    base64_bytes = base64_input.encode("utf-8")
    # Replace '-' with '+' and '_' with '/' as base64url is different than base64
    base64_bytes += b"=" * (4 - len(base64_bytes) % 4)
    base64_string = base64_bytes.decode("utf-8").replace("-", "+").replace("_", "/")
    json_payload = unquote(base64.b64decode(base64_string).decode("utf-8"))
    return json.loads(json_payload)


@dataclass
class BaseAPIClient:
    user: TUser | None = None
    host: str = PRODUCTION_API_HOST
    refresh_token_warning: bool = True
    refresh_interval_scale: float = TOKEN_REFRESH_INTERVAL_SCALE
    _relogin_timer_handle = None
    _authenticated: bool = False

    def __post_init__(self):
        if (
            isinstance(self.user, TUser)
            and self.user.jwt is not None
            and hasattr(self.user, "jwt")
        ):
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.user.jwt,
            }
        else:
            self.headers = None

    @classmethod
    def from_window_location(cls, origin):
        return cls(origin)

    def _clear_user(self):
        self.user = None
        self._remove_relogin_timer_handle()

    def _remove_relogin_timer_handle(self):
        if self._relogin_timer_handle is not None:
            self._relogin_timer_handle = None

    def _get_expire_time_from_token_in_unix_time_millis(self, token: str) -> str:
        if token is not None:
            inner_token = parse_jwt(token)
            if inner_token is not None:
                return str(1000 * inner_token["exp"])
        return str(3600 * 1000)

    def _install_token_refresh_procedure(self):
        if self.user is not None and self.user.jwt is not None:
            self._remove_relogin_timer_handle()
            expire_time_in_millis = (
                self._get_expire_time_from_token_in_unix_time_millis(self.user.jwt)
            )
            now = time.time() * 1000
            if (
                expire_time_in_millis is not None
                and float(expire_time_in_millis) > 1000 + now
            ):

                refresh_interval_in_millis = round(
                    self.refresh_interval_scale * (float(expire_time_in_millis) - now),
                    10,
                )
                self._relogin_timer_handle = Timer(
                    refresh_interval_in_millis, self._refresh_access_token
                )
        else:
            raise RuntimeError("user is none")

    def _refresh_access_token(self):
        if self.user is not None and self.user.refresh_token is not None:
            print("APIClient._refreshAccessToken - Refreshing the accessToken")
            user = vars(self.user)
            new_access_object = self._post_json("/api/batman/v1/refresh", user)
            if new_access_object.get("jwt") is not None:
                self.user = self.user
            else:
                print(
                    "APIClient._refreshAccessToken - Error no user or refresh token found!"
                )

    def _fetch_by_URL(self, url: str, options: dict):
        response = self._get_json(url, option=options)
        if response.get("ok") is False:
            status = str(response["status"])
            raise ValueError(f"Failed to load resource {url} -> Status:" + status)
        return response

    def _post_by_URL(self, url: str, options: dict):
        response = self._post_json(url, None, option=options)
        if response.get("ok") is False:
            status = str(response["status"])
            raise ValueError(
                f"Failed to load resource {url} -> Status:" + status,
                response,
            )
        return response

    def _fetch_by_path(self, path: str, options: dict):
        return self._fetch_by_URL(self.host + path, options)

    def _post_by_path(self, path: str, options: dict) -> dict:
        return self._post_by_URL(self.host + path, options)

    def _encode_auth_header(self, username: str, password: str) -> dict:
        auth_str = f"{username}:{password}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
        return {"Authorization": "Basic " + auth_b64}

    def _headers(self, headers: dict) -> dict:
        if self.user is not None and self.user.jwt is not None:
            headers["Authorization"] = f"Bearer {self.user.jwt}"
        return headers

    def _get_json(
        self,
        url: str,
        filter_json: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        full_url = str(self.host) + url
        headers = self.headers

        params_json = {}
        if filter_json is not None:
            params_json["filter"] = json.dumps(filter_json)
        if option is not None:
            params_json["option"] = json.dumps(option)
        if fields is not None:
            params_json["fields"] = json.dumps(fields)

        response = requests.get(
            url=full_url,
            headers=headers,
            params=params_json,
            timeout=timeout,
        )

        if response.status_code == requests.codes.get("ok"):
            return response.json()
        else:
            raise NovumAPIError(response.text, response.status_code)

    def _post_file(self, path: str, file: str):
        options = {"upload_file": open(file)}  # investigate how to close that
        return self._post_by_path(path, options=options)

    def _post_json(
        self,
        url: str,
        input_data: Any,
        filter_json: Optional[dict] = None,
        option: Optional[dict] = None,
        timeout: float = 4,
    ) -> dict:
        full_url = self.host + url
        headers = self.headers
        params_json = {}
        if filter_json is not None:
            params_json["filter"] = json.dumps(filter_json)
        if option is not None:
            params_json["option"] = json.dumps(option)

        if isinstance(input_data, List):
            input_data_dict = [asdict(measurement) for measurement in input_data]
        else:
            input_data_dict = asdict(input_data)
        data = json.dumps(input_data_dict, cls=DateTimeEncoder)

        response = requests.post(
            url=full_url,
            headers=headers,
            params=params_json,
            data=data,
            timeout=timeout,
        )

        if response.status_code == requests.codes.get("ok"):
            return response.json()

        else:
            raise NovumAPIError(response.text, response.status_code)

    def _put_json(
        self,
        url: str,
        input_data: Any,
        filter_json: Optional[dict] = None,
        option: Optional[dict] = None,
        timeout: float = 4,
    ) -> dict:
        full_url = self.host + url
        headers = self.headers
        params_json = {}
        if filter_json is not None:
            params_json["filter"] = json.dumps(filter_json)
        if option is not None:
            params_json["option"] = json.dumps(option)

        input_data = asdict(input_data)
        data_json = json.dumps(input_data)

        response = requests.put(
            url=full_url,
            headers=headers,
            params=params_json,
            data=data_json,
            timeout=timeout,
        )

        if response.status_code == requests.codes.get("ok"):
            return response.json()
        else:
            raise NovumAPIError(response.text, response.status_code)

    def _delete_json(
        self,
        url: str,
        filter_json: Optional[dict] = None,
        option: Optional[dict] = None,
        timeout: float = 4.0,
    ):
        full_url = self.host + url
        headers = self.headers

        params_json = {}
        if filter_json is not None:
            params_json["filter"] = json.dumps(filter_json)
        if option is not None:
            params_json["option"] = json.dumps(option)

        response = requests.delete(
            url=full_url,
            headers=headers,
            params=params_json,
            timeout=timeout,
        )
        if response.status_code <= 204:
            return response
        else:
            raise NovumAPIError(response.text, response.status_code)

    def _get_text(
        self,
        path: str,
        headers: Optional[dict] = None,
    ) -> dict:
        if headers is not None:
            headers.update({"Content-Type": "application/text"})
        else:
            headers = {"Content-Type": "application/text"}
        response = self._fetch_by_path(path, options=headers)
        text = response["text"]
        return text

    def _get_array_buffer(self, path: str, headers) -> List[int]:
        headers.update({"Content-Type": "application/text"})
        response = self._fetch_by_path(path, options=headers)
        content = response["content"]
        return [int(i) for i in content]

    def _host(self) -> str:
        return self.host

    def authenticated(self) -> bool:
        return self._authenticated

    def set_new_endpoint(self, new_end_point: str):
        self.host = new_end_point

"""
    New Client for SMS API
"""
import inspect
from http import HTTPStatus
from typing import Optional, TypeVar, Union

import requests
from requests import Response
from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict

import smsapi.resources as resources
from smsapi.error import ErrorCode, ErrorMessage, SMSException
from smsapi.models.bases import BaseModel
from smsapi.resources.base import Resource


T = TypeVar("T", bound=BaseModel)


def _is_resource_endpoint(obj):
    return isinstance(obj, Resource)


class Client:
    """
    Example usage:
        To create an instance of smsapi.Client class:

            >>> import sms
            >>> api = smsapi.Client(api_key="your api key")

        To get user details from tiktok:

            >>> res = api.tiktok.get_user_details(user_id=1234567890)
            >>> print(res.user)

        Now this api provide methods as follows:
            >>> api.instagram.get_user_details()
            >>> api.instagram.get_video_details()
            >>> api.instagram.get_video_id()
            >>> api.instagram.get_videos()
            >>> api.tiktok.get_user_details()
            >>> api.tiktok.get_video_details()
            >>> api.tiktok.get_video_id()
            >>> api.tiktok.get_videos()
    """

    BASE_URL = "https://apis.bv.media/sms/"
    DEFAULT_STATE = "SMS-PYTHON"

    instagram = resources.InstagramResource()
    tiktok = resources.TiktokResource()

    def __new__(cls, *args, **kwargs) -> "Client":
        """
        Create a new instance of Client.
        """
        self = super().__new__(cls)
        sub_resources = inspect.getmembers(self, _is_resource_endpoint)
        for name, resource in sub_resources:
            resource_cls = type(resource)
            resource = resource_cls(self)
            setattr(self, name, resource)

        return self

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> None:
        """
        Class initial

        Args:
            api_key:
                API Key for user authorized with your app.
            timeout:
                Timeout for every request.
            proxies:
                Proxies for every request.
            headers:
                Headers for every request.

        Raises:
            SMSException: Missing either credentials.
        """
        self.api_key = api_key
        self.timeout = timeout
        self.proxies = proxies
        self.headers = headers

        self.session = requests.Session()
        self.merge_headers()

        if not self._has_auth_credentials():
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Must specify api key.",
                )
            )

    def _has_auth_credentials(self) -> bool:
        """
        Check whether has credentials.
        """
        return bool(self.api_key)

    def merge_headers(self) -> None:
        """
        Merge custom headers to session.
        """
        if self.headers:
            self.session.headers = merge_setting(
                request_setting=self.session.headers,
                session_setting=self.headers,
                dict_class=CaseInsensitiveDict,
            )

    @staticmethod
    def parse_response(response: Response) -> dict:
        """
        Response parser

        Args:
            response:
                Response from the Response.

        Returns:
            Response dict data.

        Raises:
            SMSException: If response has errors.
        """
        data = response.json()
        if response.status_code != HTTPStatus.OK:
            raise SMSException(response)
        return data.get("data", {})

    def request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        enforce_auth: bool = True,
        **kwargs,
    ) -> Response:
        """
        Send request to SMS.

        Args:
            path:
                Resource or url for SMS data. such as channels, videos and so on.
            method:
                Method for the request.
            params:
                Object to send in the query string of the request.
            data:
                Object to send in the body of the request.
            json:
                Object json to send in the body of the request.
            enforce_auth:
                Whether to use user credentials.
            kwargs:
                Additional parameters for request.

        Returns:
            Response for request.

        Raises:
            SMSException: Missing credentials when need credentials.
                                Request http error.
        """
        if not path.startswith("http"):
            path = self.BASE_URL + path

        if enforce_auth:
            if not self._has_auth_credentials():
                raise SMSException(
                    ErrorMessage(
                        status_code=ErrorCode.MISSING_PARAMS,
                        message="You must provide your credentials.",
                    )
                )
            else:
                self.add_key_to_headers()

        if isinstance(json, BaseModel):
            json = json.to_dict_ignore_none()

        try:
            response = self.session.request(
                method=method,
                url=path,
                params=params,
                data=data,
                json=json,
                proxies=self.proxies,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.HTTPError as e:
            raise SMSException(
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args[0])
            ) from e
        else:
            return response

    def add_key_to_headers(self) -> None:
        """
        Add api key to headers.
        """
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def get(
        self,
        path: str,
        params: Optional[dict] = None,
        return_json: bool = False,
        model: T = None,
    ) -> Union[dict, T]:
        """
        Send a GET request to SMS.

        Args:
            path:
                Resource or url for SMS data. such as user_details,videos and so on.
            params:
                Object to send in the query string of the request.
            return_json:
                Whether to return json data.
            model:
                Model for response data.

        Returns:
            Union[dict, T]: Response data.
        """
        response = self.request(path=path, params=params)
        data = self.parse_response(response=response)
        return data if return_json else model.from_dict(data)

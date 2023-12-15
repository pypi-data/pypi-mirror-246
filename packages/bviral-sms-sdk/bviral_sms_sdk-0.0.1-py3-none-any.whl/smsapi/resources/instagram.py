"""
    Instagram resource implementation.
"""
from typing import Optional, Union

from smsapi.error import ErrorCode, ErrorMessage, SMSException
from smsapi.models import (
    InstagramUserDetailsResponse,
    InstagramVideoDetailsResponse,
    InstagramVideosResponse,
)
from smsapi.resources.base import Resource


class InstagramResource(Resource):
    """
    A resource for everything related to Instagram.
    """

    BASE_RESOURCE_ROUTE = "instagram/"

    def get_user_details(
        self,
        handle: Optional[str] = None,
        user_id: Optional[int] = None,
        target_field: Optional[str] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, InstagramUserDetailsResponse]:
        """
        Get user details by handle, user_id


        Args:
            handle (Optional[str], optional):
                handle of the user. Defaults to None.
            user_id (Optional[int], optional):
                user_id of the user. Defaults to None.
            target_field (Optional[str], optional):
                specify a field to return. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, InstagramUserDetailsResponse]: user details

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            "target_field": target_field,
            **kwargs,
        }
        if handle is not None:
            params["handle"] = handle
        elif user_id is not None:
            params["user_id"] = user_id
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of handle, user_id",
                )
            )

        return self._client.get(
            path="instagram/user_details",
            params=params,
            model=InstagramUserDetailsResponse,
            return_json=return_json,
        )

    def get_video_details(
        self,
        video_id: Optional[str] = None,
        code: Optional[str] = None,
        url: Optional[str] = None,
        fetched_after: Optional[int] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, InstagramVideoDetailsResponse]:
        """
        Get video details by video_id, code or url

        Args:
            video_id (Optional[str], optional):
                video_id of the video. Defaults to None.
            code (Optional[str], optional):
                code of the video. Defaults to None.
            url (Optional[str], optional):
                url of the video. Defaults to None.
           fetched_after (Optional[int], optional):
                fetch video details after the specified timestamp. Defaults to None.
           source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, InstagramVideoDetailsResponse]: user details

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            "fetched_after": fetched_after,
            **kwargs,
        }
        if video_id is not None:
            params["video_id"] = video_id
        elif code is not None:
            params["code"] = code
        elif url is not None:
            params["url"] = url
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of video_id, code or url",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "video_details",
            params=params,
            model=InstagramVideoDetailsResponse,
            return_json=return_json,
        )

    def get_video_id(
        self,
        url: Optional[str] = None,
        code: Optional[str] = None,
        source: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> dict:
        """
        Get video_id by url or code

        Args:
            url (Optional[str], optional):
                url of the video. Defaults to None.
            code (Optional[str], optional):
                code of the video. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.

        Returns:
            dict: video_id

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            **kwargs,
        }
        if url is not None:
            params["url"] = url
        elif code is not None:
            params["code"] = code
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of url or code",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "video_id",
            params=params,
            return_json=True,
        )

    def get_videos(
        self,
        user_id: Optional[int] = None,
        handle: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, InstagramVideosResponse]:
        """
        Get videos by user_id or handle

        Args:
            user_id (Optional[int], optional):
                user_id of the user. Defaults to None.
            handle (Optional[str], optional):
                handle of the user. Defaults to None.
            limit (Optional[int], optional):
                limit If not specified, it will return all videos. Defaults to None.
            cursor (Optional[str], optional):
                cursor for pagination. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, InstagramVideosResponse]: user details

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        if user_id is not None:
            params["user_id"] = user_id
        elif handle is not None:
            params["handle"] = handle
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of user_id or handle",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "videos",
            params=params,
            model=InstagramVideosResponse,
            return_json=return_json,
        )

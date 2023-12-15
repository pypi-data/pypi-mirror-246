"""
    Tiktok resource implementation.
"""
from typing import Optional, Union

from smsapi.error import ErrorCode, ErrorMessage, SMSException
from smsapi.models import TiktokUserDetailsResponse
from smsapi.resources.base import Resource


class TiktokResource(Resource):
    """
    A resource for everything related to Tiktok.
    """

    BASE_RESOURCE_ROUTE = "tiktok/"

    def get_user_details(
        self,
        handle: Optional[str] = None,
        user_id: Optional[int] = None,
        sec_uid: Optional[str] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, TiktokUserDetailsResponse]:
        """
        Get user details by handle, user_id or sec_uid

        Args:
            handle (Optional[str], optional):
                handle of the user. Defaults to None.
            user_id (Optional[int], optional):
                user_id of the user. Defaults to None.
            sec_uid (Optional[str], optional):
                sec_uid of the user. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, TiktokUserDetailsResponse]: user details

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            **kwargs,
        }
        if handle is not None:
            params["handle"] = handle
        elif user_id is not None:
            params["user_id"] = user_id
        elif sec_uid is not None:
            params["sec_uid"] = sec_uid
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of handle, user_id or sec_uid",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "user_details",
            params=params,
            model=TiktokUserDetailsResponse,
            return_json=return_json,
        )

    def get_video_details(
        self,
        video_id: Optional[str] = None,
        url: Optional[str] = None,
        short_url: Optional[str] = None,
        fetched_after: Optional[int] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, TiktokUserDetailsResponse]:
        """
        Get video details by video_id, url or short_url

        Args:
            video_id (Optional[str], optional):
                video_id of the video. Defaults to None.
            url (Optional[str], optional):
                url of the video. Defaults to None.
            short_url (Optional[str], optional):
                short_url of the video. Defaults to None.
            fetched_after (Optional[int], optional):
                fetch video details after the specified timestamp. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, TiktokUserDetailsResponse]: video details

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
        elif url is not None:
            params["url"] = url
        elif short_url is not None:
            params["short_url"] = short_url
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of video_id, url or short_url",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "video_details",
            params=params,
            model=TiktokUserDetailsResponse,
            return_json=return_json,
        )

    def get_video_id(
        self,
        url: Optional[str] = None,
        short_url: Optional[str] = None,
        source: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> dict:
        """
        Get video id by url or short_url

        Args:
            url (Optional[str], optional):
                url of the video. Defaults to None.
            short_url (Optional[str], optional):
                short_url of the video. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.

        Returns:
            dict: video id

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
        elif short_url is not None:
            params["short_url"] = short_url
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of url or short_url",
                )
            )

        return self._client.get(
            path="tiktok/video_id",
            params=params,
            return_json=True,
        )

    def get_videos(
        self,
        user_id: Optional[int] = None,
        sec_uid: Optional[str] = None,
        handle: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        target_field: Optional[str] = None,
        source: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, TiktokUserDetailsResponse]:
        """
        Get videos by user_id, sec_uid or handle

        Args:
            user_id (Optional[int], optional):
                user_id of the user. Defaults to None.
            sec_uid (Optional[str], optional):
                sec_uid of the user. Defaults to None.
            handle (Optional[str], optional):
                handle of the user. Defaults to None.
            limit (Optional[int], optional):
                limit If not specified, it will return all videos. Defaults to None.
            cursor (Optional[str], optional):
                cursor for pagination. Defaults to None.
            target_field (Optional[str], optional):
                target_field of the videos. Defaults to None.
            source (Optional[str], optional):
                api source. Defaults to None.
            return_json (bool, optional):
                type of return data. Defaults to False.

        Returns:
            Union[dict, TiktokUserDetailsResponse]: videos

        Raises:
            SMSException: Missing filter parameter.
                                Request not success.
        """
        params = {
            "source": source,
            "limit": limit,
            "cursor": cursor,
            "target_field": target_field,
            **kwargs,
        }
        if user_id is not None:
            params["user_id"] = user_id
        elif sec_uid is not None:
            params["sec_uid"] = sec_uid
        elif handle is not None:
            params["handle"] = handle
        else:
            raise SMSException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of user_id, sec_uid or handle",
                )
            )

        return self._client.get(
            path=self.BASE_RESOURCE_ROUTE + "videos",
            params=params,
            model=TiktokUserDetailsResponse,
            return_json=return_json,
        )

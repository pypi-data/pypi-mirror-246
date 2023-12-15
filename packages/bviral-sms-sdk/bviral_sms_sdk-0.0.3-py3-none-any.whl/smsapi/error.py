"""
    This module contains the set of SMS's exceptions.
"""
from dataclasses import dataclass
from typing import Optional, Union

from requests import Response


__all__ = ["ErrorCode", "ErrorMessage", "SMSException"]


class ErrorCode:
    """
    Error code for SMSException
    """
    HTTP_ERROR = 10000
    MISSING_PARAMS = 10001
    INVALID_PARAMS = 10002
    NEED_AUTHORIZATION = 10003
    AUTHORIZE_URL_FIRST = 10004


@dataclass
class ErrorMessage:
    """
    Error message for SMSException
    """
    status_code: Optional[int] = None
    message: Optional[str] = None


class SMSException(Exception):
    """
    SMSException is the base exception class for all exceptions in this module.
    """

    def __init__(self, response: Optional[Union[ErrorMessage, Response]]) -> None:
        self.status_code: Optional[int] = None
        self.error_type: Optional[str] = None
        self.error_details: Optional[dict] = None
        self.error_code: Optional[str] = None
        self.message: Optional[str] = None
        self.response: Optional[Union[ErrorMessage, Response]] = response
        self.error_handler()

    def error_handler(self) -> None:
        """
        Error has two big type(but not the error type.): This module's error, Api return error.
        So This will change two error to one format
        """
        if isinstance(self.response, ErrorMessage):
            self.status_code = self.response.status_code
            self.message = self.response.message
            self.error_type = "SMSException"
        elif isinstance(self.response, Response):
            res_data = self.response.json()
            if isinstance(res_data, dict):
                self.status_code = res_data["status_code"]
                self.message = res_data["message"]
                self.error_details = res_data.get("error_details")
                self.error_code = res_data.get("error_code")
            self.error_type = "SMSException"

    def __repr__(self) -> str:
        return f"{self.error_type}(status_code={self.status_code},message={self.message},error_code={self.error_code},error_details={self.error_details})"

    def __str__(self) -> str:
        return self.__repr__()

"""
    Base resource class.
"""
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from smsapi import Client  # pragma: no cover


class Resource:
    """Resource base class"""

    def __init__(self, client: Optional["Client"] = None):
        self._client = client

    @property
    def api_key(self):
        return self._client.api_key

import aiohttp

from dataclasses import dataclass
from bovine.utils import get_gmt_now

from .event_source import EventSource
from .utils import BOVINE_CLIENT_NAME


@dataclass
class BearerAuthClient:
    """Client for using Bearer authentication

    :param session: The session
    :param bearer_key: The bearer key used in the header `Authorizatoin: Bearer ${bearer_key}`
    """

    session: aiohttp.ClientSession
    bearer_key: str

    async def get(self, url: str, headers: dict = {}):
        """GET of resource"""
        accept = "application/activity+json"
        date_header = get_gmt_now()

        headers["accept"] = accept
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"
        headers["user-agent"] = BOVINE_CLIENT_NAME

        return await self.session.get(url, headers=headers)

    async def post(
        self, url: str, body: str, headers: dict = {}, content_type: str | None = None
    ):
        """POST to resource"""
        accept = "application/activity+json"
        # LABEL: ap-s2s-content-type
        if content_type is None:
            content_type = "application/activity+json"
        date_header = get_gmt_now()

        headers["accept"] = accept
        headers["content-type"] = content_type
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"

        return await self.session.post(url, data=body, headers=headers)

    def event_source(self, url: str, headers: dict = {}) -> EventSource:
        """Returns an EventSource for the server sent events given by url"""

        date_header = get_gmt_now()
        accept = "text/event-stream"

        headers["accept"] = accept
        headers["date"] = date_header
        headers["authorization"] = f"Bearer {self.bearer_key}"
        headers["user-agent"] = BOVINE_CLIENT_NAME

        return EventSource(self.session, url, headers=headers)

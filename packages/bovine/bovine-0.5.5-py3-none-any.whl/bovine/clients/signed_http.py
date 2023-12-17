import aiohttp
import bovine.clients.signed_http_methods

from bovine.crypto.types import CryptographicSecret


class SignedHttpClient:
    """Client for using HTTP Signatures"""

    def __init__(self, session, public_key_url, private_key):
        """init

        :param session: The aiohttp.ClientSession
        :param public_key_url: Used as keyId when signing
        :param private_key: The pem encoded private key
        """
        self.session = session
        self.secret = CryptographicSecret.from_pem(public_key_url, private_key)

    async def get(self, url, headers={}) -> aiohttp.ClientResponse:
        """Retrieves url using a signed get request"""
        return await bovine.clients.signed_http_methods.signed_get(
            self.session, self.secret, url, headers
        )

    async def post(self, url, body, headers={}, content_type=None):
        """Posts to url using a signed post request"""
        return await bovine.clients.signed_http_methods.signed_post(
            self.session,
            self.secret,
            url,
            body,
            headers,
            content_type=content_type,
        )

    def event_source(self, url):
        """Opens an event source to url"""
        return bovine.clients.signed_http_methods.signed_event_source(
            self.session, self.secret, url
        )

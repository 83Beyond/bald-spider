from asyncio.exceptions import TimeoutError

from aiohttp import ClientConnectionError, ClientTimeout, ClientConnectorSSLError, ClientResponseError
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError
from httpx import RemoteProtocolError, ConnectError, ReadTimeout
from anyio import EndOfStream
from httpcore import ReadError


_retry_exceptions = [
    ClientConnectionError,
    ClientTimeout,
    ClientConnectorSSLError,
    ClientResponseError,
    RemoteProtocolError,
    ReadError,
    EndOfStream,
    ConnectError,
    TimeoutError,
    ClientPayloadError,
    ReadTimeout,
    ClientConnectorError
]
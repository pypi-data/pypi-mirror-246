from __future__ import annotations

from typing import Any, AsyncIterable, Dict, Literal, Optional, TypeVar, Union

from httpx import AsyncClient
from pydantic import BaseModel, Field
from typing_extensions import ParamSpec

T = TypeVar("T")
R = TypeVar("R")
M = TypeVar("M", bound=BaseModel)
P = ParamSpec("P")


from ._decorators import robust
from ._proxy import LazyProxy

Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
Json = Union[dict[str, Any], list[Any], str, int, float, bool, None]
Scalar = Union[str, int, float, bool, None]


class APIClient(BaseModel, LazyProxy[AsyncClient]):
    """
    Generic Lazy Loading APIClient
    """

    base_url: str = Field(..., description="Base URL for the API")
    headers: Dict[str, str] = Field(
        default={"Content-Type": "application/json"},
        description="Headers for the API",
        exclude=True,
    )

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.__load__()

    def __load__(self):
        return AsyncClient(base_url=self.base_url, headers=self.headers)

    @robust
    async def fetch(
        self,
        url: str,
        *,
        method: Method,
        params: Optional[Dict[str, Scalar]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        if method in ("GET", "DELETE", "HEAD", "OPTIONS", "TRACE"):
            if headers is not None:
                self.headers.update(headers)  # pylint: disable=E1101
                headers = self.headers
            else:
                headers = self.headers
            response = await self.__load__().request(
                method=method, url=url, headers=headers, params=params
            )
        else:
            if headers is not None:
                self.headers.update(headers)  # pylint: disable=E1101
                headers = self.headers
            else:
                headers = self.headers
            response = await self.__load__().request(
                method=method, url=url, headers=headers, json=json
            )
        return response

    @robust
    async def get(
        self,
        *,
        url: str,
        params: Optional[Dict[str, Scalar]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="GET", url=url, headers=headers, params=params
        )
        return response.json()

    @robust
    async def post(
        self,
        *,
        url: str,
        params: Optional[Dict[str, Scalar]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="POST", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    @robust
    async def put(
        self,
        url: str,
        *,
        json: Optional[Json] = None,
        params: Optional[Dict[str, Scalar]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="PUT", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    @robust
    async def delete(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Scalar]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="DELETE", url=url, headers=headers, params=params
        )
        return response.json()

    @robust
    async def patch(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Scalar]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="PATCH", url=url, json=json, headers=headers, params=params
        )
        return response.json()

    @robust
    async def head(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Scalar]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="HEAD", url=url, headers=headers, params=params
        )
        return response.json()

    @robust
    async def options(
        self,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(method="OPTIONS", url=url, headers=headers)
        return response.json()

    @robust
    async def trace(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Scalar]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method="TRACE", url=url, headers=headers, params=params
        )
        return response.json()

    @robust
    async def text(
        self,
        url: str,
        *,
        method: Method = "GET",
        params: Optional[Dict[str, Scalar]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method=method, url=url, json=json, headers=headers, params=params
        )
        return response.text

    @robust
    async def blob(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Scalar]] = None,
        method: Method = "GET",
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        response = await self.fetch(
            method=method, url=url, json=json, params=params, headers=headers
        )
        return response.content

    async def stream(
        self,
        url: str,
        *,
        method: Method,
        params: Optional[Dict[str, Scalar]] = None,
        json: Optional[Json] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncIterable[bytes]:
        if headers is not None:
            self.headers.update(headers)  # pylint: disable=E1101
            headers = self.headers
        else:
            headers = self.headers
        response = await self.fetch(
            url, method=method, json=json, params=params, headers=headers
        )
        async for chunk in response.aiter_bytes():
            yield chunk

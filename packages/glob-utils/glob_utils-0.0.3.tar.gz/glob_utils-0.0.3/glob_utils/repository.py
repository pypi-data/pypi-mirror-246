from __future__ import annotations

from typing import AsyncIterable, Optional, Protocol, TypeAlias, TypeVar, Union

from pydantic import BaseModel  # pylint: disable=E0611
from typing_extensions import ParamSpec

T = TypeVar("T")
R = TypeVar("R")
M = TypeVar("M", bound=BaseModel)
P = ParamSpec("P")

Value: TypeAlias = Union[str, int, float, bool, list[str]]
Query: TypeAlias = Union[
    dict[str, Union[Value, "Query", list["Query"], list[Value]]],
    dict[str, Value],
    dict[str, list["Query"]],
]


class QueryBuilder(Protocol):
    """
    Query Builder pattern with operation overload for Firebase, DynamoDB and Pinecone.
    """

    field: str
    query: Query

    def __init__(self, *, field: str, query: Query = {}) -> None:
        ...

    def __and__(self, other: QueryBuilder) -> QueryBuilder:
        ...

    def __or__(self, other: QueryBuilder) -> QueryBuilder:
        ...

    def __eq__(self, value: Value) -> QueryBuilder:  # type: ignore
        ...

    def __ne__(self, value: Value) -> QueryBuilder:  # type: ignore
        ...

    def __gt__(self, value: Value) -> QueryBuilder:
        ...

    def __lt__(self, value: Value) -> QueryBuilder:
        ...

    def __ge__(self, value: Value) -> QueryBuilder:
        ...

    def __le__(self, value: Value) -> QueryBuilder:
        ...


class Repository(Protocol[M]):
    """
    Repository pattern for NoSQL databases
    """

    async def get(self, *, oid: str) -> Optional[M]:
        ...

    async def create(self, *, oid: str, data: M) -> M:
        ...

    async def update(self, *, oid: str, data: M) -> M:
        ...

    async def delete(self, *, oid: str) -> None:
        ...

    async def list(self) -> AsyncIterable[M]:
        ...

    async def query(self, *, query: Query) -> AsyncIterable[M]:
        ...

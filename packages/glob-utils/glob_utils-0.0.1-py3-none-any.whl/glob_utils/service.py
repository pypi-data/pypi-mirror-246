from typing import TypeAlias, TypeVar, Union

from pydantic import BaseModel  # pylint: disable=E0611

from .apiClient import APIClient
from .repository import Repository

T = TypeVar("T", bound=BaseModel)

Service: TypeAlias = Union[APIClient, Repository[T]]

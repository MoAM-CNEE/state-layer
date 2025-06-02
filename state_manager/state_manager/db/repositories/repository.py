from abc import ABC, abstractmethod

from typing import List, Optional
from sqlalchemy.orm import Session


class Repository(ABC):
    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def get_by_key(self, **kwargs) -> Optional[object]:
        pass

    @abstractmethod
    def get_by_query(self, query: str) -> List[object]:
        pass

    @abstractmethod
    def create(self, **kwargs) -> object:
        pass

    @abstractmethod
    def update(self, **kwargs) -> Optional[object]:
        pass

    @abstractmethod
    def delete(self, entity: object) -> None:
        pass

    def extract_kwargs(self, kwargs: dict, fields: List[str]) -> dict:
        return {field: kwargs.get(field) for field in fields if field in kwargs}

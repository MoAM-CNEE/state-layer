from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session

from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService


class EntityService(ABC):
    def __init__(self, db: Session, mirror_manager_service: MirrorManagerService):
        self.db = db
        self.mirror_manager_service = mirror_manager_service

    # TODO: Use kwargs for abstract methods OR don't use a common abstract class

    @abstractmethod
    async def create(self, change_id: int, definition: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, change_id: int, filter_by: str, lambdas: Dict[str, str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def delete(self, change_id: int, filter_by: str) -> Dict[str, Any]:
        pass

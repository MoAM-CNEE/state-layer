from typing import Dict, Any

from sqlalchemy.orm.session import Session

from state_manager.db.repositories.rule_repository import RuleRepository
from state_manager.entity.entity_service import EntityService
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService


class RuleService(EntityService):
    def __init__(self, db: Session, mirror_manager_service: MirrorManagerService):
        super().__init__(db, mirror_manager_service)
        self.rule_repository = RuleRepository(db)

    async def create(self, change_id: int, entity_definition: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    async def update(self, change_id: int, filter_by: str, lambdas: Dict[str, str]) -> Dict[str, Any]:
        raise NotImplementedError()

    async def delete(self, change_id: int, filter_by: str) -> Dict[str, Any]:
        raise NotImplementedError()

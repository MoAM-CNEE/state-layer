from typing import Dict, Any

from sqlalchemy.orm.session import Session

from state_manager.api.request_models import ControlPlaneApplyRQ, ControlPlaneDeleteRQ
from state_manager.db.repositories.environment_entity_repository import EnvironmentEntityRepository, \
    EnvironmentEntityLabelRepository
from state_manager.entity.entity_service import EntityService
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService


class EnvironmentEntityService(EntityService):
    def __init__(self, db: Session, mirror_manager_service: MirrorManagerService):
        super().__init__(db, mirror_manager_service)
        self.environment_entity_repository = EnvironmentEntityRepository(db)
        self.environment_entity_label_repository = EnvironmentEntityLabelRepository(db)

    async def create(self, change_id: int, entity_definition: Dict[str, Any]) -> Dict[str, Any]:
        await self.mirror_manager_service.apply(ControlPlaneApplyRQ(change_id=0, entity_definition=entity_definition))
        api_version, kind, name, namespace = self._get_entity_key(entity_definition)
        self.environment_entity_repository.create(
            api_version=api_version,
            kind=kind,
            name=name,
            namespace=namespace,
            definition=entity_definition,
        )

    async def update(self, change_id: int, filter_by: str, lambdas: Dict[str, str]) -> Dict[str, Any]:
        entities = self.environment_entity_repository.get_by_filter(filter_by)
        for entity in entities:
            # TODO: Apply lambdas
            await self.mirror_manager_service.apply(ControlPlaneApplyRQ(change_id=0, entity_definition=entity.definition))
            api_version, kind, name, namespace = self._get_entity_key(entity.definition)
            self.environment_entity_repository.update(api_version, kind, name, namespace)

    async def delete(self, change_id: int, filter_by: str) -> Dict[str, Any]:
        entities = self.environment_entity_repository.get_by_filter(filter_by)
        for entity in entities:
            await self.mirror_manager_service.delete(
                ControlPlaneDeleteRQ(change_id=0, api_version=entity.api_version, kind=entity.kind,
                                     name=entity.name, namespace=entity.namespace))
            self.environment_entity_repository.delete(entity)

    def _get_entity_key(self, entity_definition: Dict[str, Any]) -> tuple[str, str, str, str]:
        entity_metadata = entity_definition.get('metadata')
        return (entity_definition.get('apiVersion'), entity_definition.get('kind'), entity_metadata.get('name', ''),
                entity_metadata.get('namespace', ''))

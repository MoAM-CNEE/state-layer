from abc import ABC, abstractmethod
from typing import Dict, Any

import jq
from sqlalchemy.orm import Session

from state_manager.api.request_models import ApplyOnControlPlaneRQ, DeleteFromControlPlaneRQ
from state_manager.db.repositories.entity_label_repository import EntityLabelRepository
from state_manager.db.repositories.entity_repository import EntityRepository
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService


class EntityService:
    def __init__(self, db: Session, mirror_manager_service: MirrorManagerService):
        self.mirror_manager_service = mirror_manager_service
        self.entity_repository = EntityRepository(db)
        self.entity_label_repository = EntityLabelRepository(db)

    async def create(self, change_id: int, definition: Dict[str, Any]) -> Dict[str, Any]:
        await self.mirror_manager_service.apply(
            ApplyOnControlPlaneRQ(change_id=change_id, entity_definition=definition))
        api_version, kind, name, namespace = self._get_entity_key(definition)
        self.entity_repository.create(
            api_version=api_version,
            kind=kind,
            name=name,
            namespace=namespace,
            definition=definition,
        )

    async def update(self, change_id: int, query: str, lambdas: Dict[str, str]) -> Dict[str, Any]:
        entities = self.entity_repository.get_by_filter(query)
        print(f"Found {len(entities)} entities to update with {len(lambdas)} lambdas")
        for entity in entities:
            for field, right_side in lambdas.items():
                original_value = self._get_value_from_dict_by_jq_key(entity.definition, field)
                jq_expression = f"{field} |= {right_side}"
                try:
                    updated_definition = jq.compile(jq_expression).input(entity.definition).first()
                    if updated_definition:
                        entity.definition = updated_definition
                        updated_value = self._get_value_from_dict_by_jq_key(entity.definition, field)
                        print(
                            f"Updated field '{field}' from '{original_value}' to '{updated_value}' with jq expression '{jq_expression}'")
                    else:
                        print(f"No result returned for jq expression '{jq_expression}'")
                except Exception as e:
                    print(f"Error applying jq expression '{jq_expression}' on field '{field}': {e}")
            await self.mirror_manager_service.apply(
                ApplyOnControlPlaneRQ(change_id=change_id, entity_definition=entity.definition)
            )
            api_version, kind, name, namespace = self._get_entity_key(entity.definition)
            self.entity_repository.update(
                api_version=api_version,
                kind=kind,
                name=name,
                namespace=namespace,
                new_definition=entity.definition
            )

    async def delete(self, change_id: int, query: str) -> Dict[str, Any]:
        entities = self.entity_repository.get_by_filter(query)
        for entity in entities:
            await self.mirror_manager_service.delete(
                DeleteFromControlPlaneRQ(change_id=change_id, api_version=entity.api_version, kind=entity.kind,
                                     name=entity.name, namespace=entity.namespace))
            self.entity_repository.delete(entity)

    def _get_entity_key(self, definition: Dict[str, Any]) -> tuple[str, str, str, str]:
        metadata = definition.get('metadata')
        return (definition.get('apiVersion'), definition.get('kind'), metadata.get('name', ''),
                metadata.get('namespace', ''))

    def _get_value_from_dict_by_jq_key(self, _dict: dict, jq_key: str) -> str:
        keys = jq_key[1:].split(".")  # Omit leading .
        target = _dict
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        last_key = keys[-1]
        value = target.get(last_key)
        return value

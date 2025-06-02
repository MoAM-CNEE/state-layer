import json
from typing import List, Optional

from sqlalchemy import text

from state_manager.db.models import Entity
from state_manager.db.repositories.repository import Repository


class EntityRepository(Repository):
    def get_by_key(self, **kwargs) -> Optional[Entity]:
        fields = ['api_version', 'kind', 'name', 'namespace']
        filters = self.extract_kwargs(kwargs, fields)
        return self.db.query(Entity).query(**filters).first()

    def get_by_query(self, query: str) -> List[Entity]:
        result = self.db.execute(text(query)).fetchall()
        environment_entities = []
        for row in result:
            row_dict = dict(row._mapping)
            row_dict['id'] = int(row_dict['id'])
            row_dict['definition'] = json.loads(row_dict['definition'])
            entity = Entity(**row_dict)
            merged_entity = self.db.merge(entity)
            environment_entities.append(merged_entity)
        self.db.commit()
        return environment_entities

    def create(self, **kwargs) -> Entity:
        fields = ['api_version', 'kind', 'name', 'namespace', 'definition']
        extracted = self.extract_kwargs(kwargs, fields)
        entity = Entity(**extracted)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, **kwargs) -> Optional[Entity]:
        fields = ['api_version', 'kind', 'name', 'namespace', 'new_definition']
        extracted = self.extract_kwargs(kwargs, fields)
        entity = self.get_by_key(**extracted)
        if not entity:
            return None
        if extracted.get('new_definition') is not None:
            entity.definition = extracted['new_definition']
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: Entity) -> None:
        self.db.delete(entity)
        self.db.commit()

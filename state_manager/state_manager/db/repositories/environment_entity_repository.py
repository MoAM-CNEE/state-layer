import json
from typing import List, Optional

from sqlalchemy import text

from state_manager.db.models import EnvironmentEntity
from state_manager.db.repositories.repository import Repository


class EnvironmentEntityRepository(Repository):
    def get_by(self, **kwargs) -> Optional[EnvironmentEntity]:
        fields = ['api_version', 'kind', 'name', 'namespace']
        filters = self.extract_kwargs(kwargs, fields)
        return self.db.query(EnvironmentEntity).filter_by(**filters).first()

    def get_by_filter(self, filter_by: str) -> List[EnvironmentEntity]:
        result = self.db.execute(text(filter_by)).fetchall()
        environment_entities = []
        for row in result:
            row_dict = dict(zip(['id', 'api_version', 'kind', 'name', 'namespace', 'definition'], row))
            row_dict['definition'] = json.loads(row_dict['definition'])
            entity = EnvironmentEntity(**row_dict)
            merged_entity = self.db.merge(entity)
            environment_entities.append(merged_entity)
        self.db.commit()
        return environment_entities

    def create(self, **kwargs) -> EnvironmentEntity:
        fields = ['api_version', 'kind', 'name', 'namespace', 'definition']
        extracted = self.extract_kwargs(kwargs, fields)
        entity = EnvironmentEntity(**extracted)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, **kwargs) -> Optional[EnvironmentEntity]:
        fields = ['api_version', 'kind', 'name', 'namespace', 'new_definition']
        extracted = self.extract_kwargs(kwargs, fields)
        entity = self.get_by(**extracted)
        if not entity:
            return None
        if extracted.get('new_definition') is not None:
            entity.definition = extracted['new_definition']
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: EnvironmentEntity) -> None:
        self.db.delete(entity)
        self.db.commit()

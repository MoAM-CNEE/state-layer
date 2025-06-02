from typing import List, Optional

from sqlalchemy import text

from state_manager.db.models import EntityLabel
from state_manager.db.repositories.repository import Repository


class EntityLabelRepository(Repository):
    def get_by(self, **kwargs) -> Optional[EntityLabel]:
        extracted = self.extract_kwargs(kwargs, ['label_id'])
        label_id = extracted.get('label_id')
        return self.db.query(EntityLabel).filter(EntityLabel.id == label_id).first()

    def get_by_filter(self, query: str) -> List[EntityLabel]:
        result = self.db.execute(text(query)).fetchall()
        environment_labels = []
        for row in result:
            label = EntityLabel(id=row[0], entity_id=row[1], name=row[2], value=row[3])
            environment_labels.append(label)
        return environment_labels

    def create(self, **kwargs) -> EntityLabel:
        extracted = self.extract_kwargs(kwargs, ['entity_id', 'name', 'value'])
        label = EntityLabel(
            entity_id=extracted.get('entity_id'),
            name=extracted.get('name'),
            value=extracted.get('value')
        )
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label

    def update(self, **kwargs) -> Optional[EntityLabel]:
        extracted = self.extract_kwargs(kwargs, ['label_id', 'new_name', 'new_value'])
        label_id = extracted.get('label_id')
        new_name = extracted.get('new_name')
        new_value = extracted.get('new_value')
        label = self.get_by(label_id=label_id)
        if not label:
            return None
        if new_name is not None:
            label.name = new_name
        if new_value is not None:
            label.value = new_value
        self.db.commit()
        self.db.refresh(label)
        return label

    def delete(self, entity: EntityLabel) -> None:
        self.db.delete(entity)
        self.db.commit()

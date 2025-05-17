from sqlalchemy.orm import Session
from state_manager.db.models import EnvironmentEntity, EnvironmentEntityLabel

class EnvironmentEntityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, entity_id: int):
        return self.db.query(EnvironmentEntity).filter(EnvironmentEntity.id == entity_id).first()

    def create(self, entity_id: int, api_version: str, kind: str, name: str, namespace: str, definition: dict):
        entity = EnvironmentEntity(
            id=entity_id,
            api_version=api_version,
            kind=kind,
            name=name,
            namespace=namespace,
            definition=definition,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def list_all(self):
        return self.db.query(EnvironmentEntity).all()


class EnvironmentEntityLabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, label_id: int):
        return self.db.query(EnvironmentEntityLabel).filter(EnvironmentEntityLabel.id == label_id).first()

    def create(self, label_id: int, entity_id: int, name: str, value: str):
        label = EnvironmentEntityLabel(
            id=label_id,
            environment_entity_id=entity_id,
            name=name,
            value=value
        )
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label

    def list_all(self):
        return self.db.query(EnvironmentEntityLabel).all()

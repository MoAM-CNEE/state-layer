from sqlalchemy.orm.session import Session

from state_manager.entity.entity_service import EntityService
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService
from state_manager.api.request_models import EntityType
from state_manager.entity.environment_entity_service import EnvironmentEntityService
from state_manager.entity.metric_service import MetricService
from state_manager.entity.rule_service import RuleService


class EntityServiceFactory:
    def __init__(self, db: Session, mirror_manager_service: MirrorManagerService):
        self.db = db
        self.mirror_manager_service = mirror_manager_service

    def get(self, entity_type: EntityType) -> EntityService:
        if entity_type == EntityType.RULE:
            return RuleService(self.db, self.mirror_manager_service)
        elif entity_type == EntityType.METRIC:
            return MetricService(self.db, self.mirror_manager_service)
        else:
            return EnvironmentEntityService(self.db, self.mirror_manager_service)

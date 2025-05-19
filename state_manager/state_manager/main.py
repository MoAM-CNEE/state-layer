from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from state_manager.api.request_models import EntityCreateActionRQ, EntityUpdateActionRQ, EntityDeleteActionRQ
from state_manager.db.repositories.environment_entity_label_repository import EnvironmentEntityLabelRepository
from state_manager.db.repositories.environment_entity_repository import EnvironmentEntityRepository
from state_manager.db.repositories.metric_repository import MetricRepository
from state_manager.db.repositories.rule_repository import RuleRepository
from state_manager.db.session import DatabaseSessionManager
from state_manager.entity.entity_service_factory import EntityServiceFactory
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService

app = FastAPI()
db_manager = DatabaseSessionManager()
mirror_manager_service = MirrorManagerService()


def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


def get_mirror_manager_service() -> MirrorManagerService:
    return mirror_manager_service


def get_entity_service_factory(db: Session = Depends(get_db), mirror_manager_service: MirrorManagerService = Depends(
    get_mirror_manager_service)) -> EntityServiceFactory:
    return EntityServiceFactory(db, mirror_manager_service)


@app.post("/entity/create")
async def create_entity(rq: EntityCreateActionRQ,
                        entity_service_factory: EntityServiceFactory = Depends(get_entity_service_factory)):
    return await entity_service_factory.get(rq.type).create(rq.change_id, rq.entity_definition)


@app.put("/entity/update")
async def update_entity(rq: EntityUpdateActionRQ,
                        entity_service_factory: EntityServiceFactory = Depends(get_entity_service_factory)):
    return await entity_service_factory.get(rq.type).update(rq.change_id, rq.filter_by, rq.lambdas)


@app.delete("/entity/delete")
async def delete_entity(rq: EntityDeleteActionRQ,
                        entity_service_factory: EntityServiceFactory = Depends(get_entity_service_factory)):
    return await entity_service_factory.get(rq.type).delete(rq.change_id, rq.filter_by)

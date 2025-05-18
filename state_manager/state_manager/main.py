from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from state_manager.api.request_models import EntityCreateActionRQ, EntityUpdateActionRQ, EntityDeleteActionRQ
from state_manager.db.repositories.environment_entity_repository import EnvironmentEntityRepository, \
    EnvironmentEntityLabelRepository
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


@app.get("/rules/{rule_id}")
def read_rule(rule_id: int, db: Session = Depends(get_db)):
    repo = RuleRepository(db)
    rule = repo.get_by_id(rule_id)
    return rule or {"error": "Rule not found"}


@app.post("/rules/")
def create_rule(rule_id: int, condition: str, action: str, db: Session = Depends(get_db)):
    repo = RuleRepository(db)
    return repo.create(rule_id, condition, action)


@app.get("/metrics/{metric_id}")
def read_metric(metric_id: int, db: Session = Depends(get_db)):
    repo = MetricRepository(db)
    metric = repo.get_by_id(metric_id)
    return metric or {"error": "Metric not found"}


@app.post("/metrics/")
def create_metric(metric_id: int, name: str, query: str, db: Session = Depends(get_db)):
    repo = MetricRepository(db)
    return repo.create(metric_id, name, query)


@app.get("/entities/{entity_id}")
def read_entity(entity_id: int, db: Session = Depends(get_db)):
    repo = EnvironmentEntityRepository(db)
    entity = repo.get_by_id(entity_id)
    return entity or {"error": "EnvironmentEntity not found"}


@app.post("/entities/")
def create_entity(entity_id: int, api_version: str, kind: str, name: str, namespace: str, definition: dict,
                  db: Session = Depends(get_db)):
    repo = EnvironmentEntityRepository(db)
    return repo.create(entity_id, api_version, kind, name, namespace, definition)


@app.get("/entity-labels/{label_id}")
def read_label(label_id: int, db: Session = Depends(get_db)):
    repo = EnvironmentEntityLabelRepository(db)
    label = repo.get_by_id(label_id)
    return label or {"error": "Label not found"}


@app.post("/entity-labels/")
def create_label(label_id: int, entity_id: int, name: str, value: str, db: Session = Depends(get_db)):
    repo = EnvironmentEntityLabelRepository(db)
    return repo.create(label_id, entity_id, name, value)


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

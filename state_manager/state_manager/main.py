from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from state_manager.db.repositories.environment_repository import EnvironmentEntityRepository, \
    EnvironmentEntityLabelRepository
from state_manager.db.repositories.metric_repository import MetricRepository
from state_manager.db.repositories.rule_repository import RuleRepository
from state_manager.db.session import DatabaseSessionManager

app = FastAPI()
db_manager = DatabaseSessionManager()


def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


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
def create_entity(entity_id: int, name: str, namespace: str, definition: dict, db: Session = Depends(get_db)):
    repo = EnvironmentEntityRepository(db)
    return repo.create(entity_id, name, namespace, definition)


@app.get("/entity-labels/{label_id}")
def read_label(label_id: int, db: Session = Depends(get_db)):
    repo = EnvironmentEntityLabelRepository(db)
    label = repo.get_by_id(label_id)
    return label or {"error": "Label not found"}


@app.post("/entity-labels/")
def create_label(label_id: int, entity_id: int, name: str, value: str, db: Session = Depends(get_db)):
    repo = EnvironmentEntityLabelRepository(db)
    return repo.create(label_id, entity_id, name, value)

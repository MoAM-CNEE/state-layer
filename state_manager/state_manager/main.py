from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

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

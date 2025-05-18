from sqlalchemy.orm import Session
from state_manager.db.models import Rule

class RuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rule_id: int):
        return self.db.query(Rule).filter(Rule.id == rule_id).first()

    def create(self, condition: str, action: str):
        rule = Rule(_condition=condition, _action=action)
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def list_all(self):
        return self.db.query(Rule).all()

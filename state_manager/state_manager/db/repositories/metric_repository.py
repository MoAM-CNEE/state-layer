from sqlalchemy.orm import Session
from state_manager.db.models import Metric

class MetricRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, metric_id: int):
        return self.db.query(Metric).filter(Metric.id == metric_id).first()

    def create(self, name: str, query: str):
        metric = Metric(name=name, query=query)
        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)
        return metric

    def list_all(self):
        return self.db.query(Metric).all()

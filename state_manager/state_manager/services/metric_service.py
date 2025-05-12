from schemas.metric import RetrieveMetricRQ, RetrieveMetricRS
from services.system_entity_service import SystemEntityService


class MetricService(SystemEntityService):
    def persist(self):
        pass

    def retrieve(self, retrieve_rq: RetrieveMetricRQ) -> RetrieveMetricRS:
        result = self.run_query(f"SELECT * FROM metric WHERE name = '{retrieve_rq.name}'")
        return result

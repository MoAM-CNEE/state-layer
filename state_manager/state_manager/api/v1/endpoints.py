from fastapi import APIRouter

from schemas.metric import RetrieveMetricRQ
from services.metric_service import MetricService

router = APIRouter()
metric_service = MetricService()

@router.get("/metric")
async def get_metric():
    return metric_service.retrieve(RetrieveMetricRQ(name="cluster-memory-usage"))

from enum import Enum

from pydantic import BaseModel
from typing import Dict, Any, Optional


class ControlPlaneApplyRQ(BaseModel):
    change_id: int
    entity_definition: Dict[str, Any]


class ControlPlaneDeleteRQ(BaseModel):
    change_id: int
    api_version: str
    kind: str
    name: str
    namespace: Optional[str] = None


class EntityType(str, Enum):
    RULE = "RULE"
    METRIC = "METRIC"
    ENVIRONMENT_ENTITY = "ENVIRONMENT_ENTITY"


class EntityCreateActionRQ(BaseModel):
    change_id: int
    type: EntityType
    entity_definition: Dict[str, Any]


class EntityUpdateActionRQ(BaseModel):
    change_id: int
    type: EntityType
    filter_by: str
    lambdas: Dict[str, str]


class EntityDeleteActionRQ(BaseModel):
    change_id: int
    type: EntityType
    filter_by: str

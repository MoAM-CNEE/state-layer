from enum import Enum

from pydantic import BaseModel
from typing import Dict, Any, Optional


class ApplyOnControlPlaneRQ(BaseModel):
    change_id: int
    entity_definition: Dict[str, Any]


class DeleteFromControlPlaneRQ(BaseModel):
    change_id: int
    api_version: str
    kind: str
    name: str
    namespace: Optional[str] = None


class CreateEntityActionRQ(BaseModel):
    change_id: int
    definition: Dict[str, Any]


class UpdateEntityActionRQ(BaseModel):
    change_id: int
    filter_by: str
    lambdas: Dict[str, str]


class DeleteEntityActionRQ(BaseModel):
    change_id: int
    filter_by: str

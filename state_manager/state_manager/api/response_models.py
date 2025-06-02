from typing import Any

from pydantic import BaseModel, ConfigDict


class ApplyOnControlPlaneRS(BaseModel):
    change_id: int
    updated: bool


class DeleteFromControlPlaneRS(BaseModel):
    change_id: int


class EntityDTO(BaseModel):
    id: int
    api_version: str
    kind: str
    name: str
    namespace: str
    definition: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class ReadEntityActionRS(BaseModel):
    entities: list[EntityDTO]

# TODO: Entity operations RSs

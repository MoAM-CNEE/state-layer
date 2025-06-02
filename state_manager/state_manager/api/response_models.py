from pydantic import BaseModel

from state_manager.dto.entity import EntityDTO


class ApplyOnControlPlaneRS(BaseModel):
    change_id: int
    updated: bool


class DeleteFromControlPlaneRS(BaseModel):
    change_id: int


class ReadEntityActionRS(BaseModel):
    entities: list[EntityDTO]

# TODO: Entity operations RSs

from typing import Any

from pydantic import BaseModel, ConfigDict


class EntityDTO(BaseModel):
    id: int
    api_version: str
    kind: str
    name: str
    namespace: str
    definition: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

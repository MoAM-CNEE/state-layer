from pydantic import BaseModel


class RetrieveRQ(BaseModel):
    pass


class RetrieveRS(BaseModel):
    id: int

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from state_manager.api.request_models import CreateEntityActionRQ, UpdateEntityActionRQ, DeleteEntityActionRQ, \
    ReadEntityActionRQ
from state_manager.api.response_models import ReadEntityActionRS, EntityDTO
from state_manager.db.session import DatabaseSessionManager
from state_manager.entity.entity_service import EntityService
from state_manager.mirror_layer.mirror_manager_service import MirrorManagerService

app = FastAPI()
db_manager = DatabaseSessionManager()
mirror_manager_service = MirrorManagerService()


def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


def get_mirror_manager_service() -> MirrorManagerService:
    return mirror_manager_service


def get_entity_service(db: Session = Depends(get_db), mirror_manager_service: MirrorManagerService = Depends(
    get_mirror_manager_service)) -> EntityService:
    return EntityService(db, mirror_manager_service)


@app.post("/entity/create")
async def create_entity(rq: CreateEntityActionRQ,
                        entity_service: EntityService = Depends(get_entity_service)):
    return await entity_service.create(rq.change_id, rq.definition, rq.trigger_mirror_manager)


@app.put("/entity/update")
async def update_entity(rq: UpdateEntityActionRQ,
                        entity_service: EntityService = Depends(get_entity_service)):
    return await entity_service.update(rq.change_id, rq.query, rq.lambdas, rq.trigger_mirror_manager)


@app.delete("/entity/delete")
async def delete_entity(rq: DeleteEntityActionRQ,
                        entity_service: EntityService = Depends(get_entity_service)):
    return await entity_service.delete(rq.change_id, rq.query, rq.trigger_mirror_manager)


@app.get("/entity/read", response_model=ReadEntityActionRS)
async def read_entity(rq: ReadEntityActionRQ,
                      entity_service: EntityService = Depends(get_entity_service)):
    entities = await entity_service.read(rq.query)
    return ReadEntityActionRS(entities=[EntityDTO.model_validate(e) for e in entities])

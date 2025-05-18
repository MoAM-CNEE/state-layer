import httpx

from state_manager.api.request_models import ControlPlaneApplyRQ, ControlPlaneDeleteRQ
from state_manager.api.response_models import ControlPlaneApplyRS, ControlPlaneDeleteRS


class MirrorManagerService:
    def __init__(self, base_url: str = "http://mirror-manager-svc.mirror-layer.svc.cluster.local:8000"):
        self.base_url = base_url

    async def apply(self, request: ControlPlaneApplyRQ) -> ControlPlaneApplyRS:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/apply", json=request.model_dump())
            response.raise_for_status()
            return ControlPlaneApplyRS(**response.json())

    async def delete(self, request: ControlPlaneDeleteRQ) -> ControlPlaneDeleteRS:
        async with httpx.AsyncClient() as client:
            response = await client.request("DELETE", f"{self.base_url}/delete", json=request.model_dump())
            response.raise_for_status()
            return ControlPlaneDeleteRS(**response.json())

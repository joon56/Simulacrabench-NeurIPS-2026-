"""Pinned real SDK adapter; tests replace only external call endpoints."""
import asyncio
from datetime import datetime, timezone
from google.protobuf.empty_pb2 import Empty
from modal_proto import api_pb2 as pb
from controller_core import install_pins
from live_binding import SDK, image_from_id


class Endpoint:
    def __init__(self, client_factory=None, image_builder=None, sandbox_factory=None):
        self.client_factory = client_factory or SDK.Client.from_env
        self.image_builder = image_builder or self._build
        self.sandbox_factory = sandbox_factory or SDK.Sandbox.create
        self.client = self.app = self.image = self.sandbox = None

    async def connect(self):
        self.client = await self.client_factory()
        if self.client._cancellation_context_event_loop is not asyncio.get_running_loop():
            raise RuntimeError("SDK event-loop mismatch")
        response = await self.client._stub.WorkspaceNameLookup(Empty())
        if not isinstance(response, pb.WorkspaceNameLookupResponse) or response.username != "joon56":
            raise RuntimeError("Workspace mismatch")
        return response.username

    async def billing(self):
        request = pb.WorkspaceBillingSummaryRequest()
        request.start_timestamp.FromDatetime(datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        response = await self.client._stub.WorkspaceBillingSummary(request)
        if not isinstance(response, pb.WorkspaceBillingSummaryResponse):
            raise TypeError("Wrong normal billing response")
        return response

    def base_stream(self, image_id):
        return self.client._stub.ImageJoinStreaming.unary_stream(pb.ImageJoinStreamingRequest(image_id=image_id, timeout=3))

    async def image_info(self, image_id):
        return await self.client._stub.ImageFromId(pb.ImageFromIdRequest(image_id=image_id))

    async def app_lookup(self, name, create):
        self.app = await SDK.App.lookup(name, client=self.client, environment_name="main", create_if_missing=create)
        return self.app.app_id

    async def _build(self, image, app):
        with SDK.enable_output():
            return await image.build(app)

    async def build(self, base_id, pins, deadline):
        self.image = image_from_id(base_id, self.client).run_function(install_pins,
            args=(pins, deadline), cpu=(1, 1), memory=(8192, 8192), timeout=600, include_source=False)
        if not isinstance(self.image, SDK.Image):
            raise TypeError("Image not raw async")
        await self.image_builder(self.image, self.app)
        return self.image.object_id

    async def sandbox_create(self, name):
        self.sandbox = await self.sandbox_factory("sleep", "2400", app=self.app,
            name=name, image=self.image, timeout=2400, gpu="H100!", cpu=(1, 1),
            memory=(15258, 15258), runtime="gvisor", block_network=True,
            secrets=[], include_oidc_identity_token=False, encrypted_ports=[], h2_ports=[],
            unencrypted_ports=[], env={"OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2",
                "OPENBLAS_NUM_THREADS": "2", "NUMEXPR_NUM_THREADS": "2", "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1"}, client=self.client)
        return self.sandbox.object_id

    async def sandbox_recover(self, name):
        # Source-defined read-only name lookup; no create after ambiguous reply.
        self.sandbox = await SDK.Sandbox.from_name(self.app.name, name, client=self.client, environment_name="main")
        return self.sandbox.object_id

    async def stop_app(self, app_id):
        return await self.client._stub.AppStop(pb.AppStopRequest(app_id=app_id, source=pb.APP_STOP_SOURCE_CLI))

    async def app_info(self, app_id):
        return await self.client._stub.AppGetInfo(pb.AppGetInfoRequest(app_id=app_id))

    async def tasks(self, app_id):
        return await self.client._stub.TaskList(pb.TaskListRequest(app_id=app_id))

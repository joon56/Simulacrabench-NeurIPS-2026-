"""Pinned SDK1.6.0 raw async binding; import alone does not authenticate."""
from types import SimpleNamespace
from modal.client import _Client
from modal._workspace import _Workspace
from modal.app import _App
from modal._image import _Image
from modal.sandbox import _Sandbox
from modal.output import enable_output
from modal._utils.async_utils import synchronizer
from modal_proto import api_pb2

SDK = SimpleNamespace(Client=_Client, Workspace=_Workspace, App=_App, Image=_Image,
                      Sandbox=_Sandbox, pb=api_pb2, enable_output=enable_output)


def image_from_id(image_id, client):
    # SDK1.6.0 from_id is a synchronous handle constructor returning a public
    # wrapper, even on _Image. Translate the handle before raw async use.
    return synchronizer._translate_in(_Image.from_id(image_id, client=client))

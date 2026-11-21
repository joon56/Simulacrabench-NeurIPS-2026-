"""Actual installed protobuf response validation; no fabricated module enum."""
from modal_proto import api_pb2 as pb
from contract import sha


async def validate_base(stream, expected_sha):
    result = None
    async for row in stream:
        if not isinstance(row, pb.ImageJoinStreamingResponse):
            raise TypeError("Wrong image stream response type")
        if row.result.status:
            if row.result.status != pb.GenericResult.GENERIC_STATUS_SUCCESS:
                raise RuntimeError("Base image unsuccessful status: " + str(row.result.status))
            if result is not None and result.SerializeToString() != row.result.SerializeToString():
                raise ValueError("Conflicting image results")
            result = row.result
    if result is None:
        raise RuntimeError("Empty or unspecified image result")
    if sha(bytes(result.data)) != expected_sha:
        raise ValueError("Base result identity mismatch")
    return {"status": int(result.status), "result_sha256": sha(bytes(result.data))}


def validate_image_id(response, expected):
    if not isinstance(response, pb.ImageFromIdResponse) or response.image_id != expected:
        raise ValueError("ImageFromId response mismatch")
    return sha(response.metadata.SerializeToString())


def termination_observation(info, tasks):
    if not isinstance(info, pb.AppGetInfoResponse) or not isinstance(tasks, pb.TaskListResponse):
        raise TypeError("Wrong termination response type")
    return {"state": int(info.info.lifecycle.app_state), "tasks": len(tasks.tasks),
            "confirmed": info.info.lifecycle.app_state == pb.APP_STATE_STOPPED and len(tasks.tasks) == 0}

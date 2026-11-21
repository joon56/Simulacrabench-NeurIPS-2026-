"""Read installed SDK protobuf field names only; no client or model invocation."""
import json
from modal_proto import api_pb2 as p

names = ["EnvironmentGetBudgetRequest", "EnvironmentGetBudgetResponse",
         "WorkspaceSettingsResponse", "WorkspaceBillingSummaryResponse",
         "ImageGetOrCreateRequest", "Image", "AppStopRequest"]
print(json.dumps({n: [{"name": f.name, "type": f.type,
                      "message": f.message_type.full_name if f.message_type else None}
                     for f in getattr(p, n).DESCRIPTOR.fields] for n in names}, indent=2))
print(json.dumps({"billing_budget_credit_message_names": [n for n in p.DESCRIPTOR.message_types_by_name
                  if any(s in n.lower() for s in ("budget", "credit", "spend"))]}))

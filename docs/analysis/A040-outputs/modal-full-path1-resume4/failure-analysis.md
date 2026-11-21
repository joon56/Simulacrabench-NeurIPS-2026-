# Resume4: remote builder module unavailable

Observed failure: `ModuleNotFoundError: No module named 'controller_core'`.
The captured build log identifies image `im-LEPHgU6tpUAuu3H17E5rr5` and the step
running `install_pins`. Modal's remote user-code import fails before the function
body executes. Worker receives ImageBuildError and immediately enters cleanup.

Source evidence: frozen sdk_endpoint.py imports install_pins from controller_core
and calls Image.run_function with include_source=False. Installed SDK1.6.0
_image.py:2772 constructs FunctionSourceInfo(raw_f); lines2774-2788 retain the
function source information and pass include_source to its builder function.
Remote traceback calls importlib.import_module(function_def.module_name) and
cannot resolve controller_core. The later12-file Sandbox payload transfer does
not make this module available during the earlier dependency-image build.

This supports a located builder source-delivery/import contract failure. It does
not establish a pin incompatibility, H100 availability/runtime failure, OOM,
native boundary failure or model/effect result. No installer-complete Linux lock,
driver observation, payload parity check, boundary or scientific result exists.

The local orchestration tests had replaced the image-build endpoint. They covered
local SDK handle construction and downstream protocol behavior, not remote import
of the builder's defining module. Historical local PASSes are preserved within
those scopes; they do not contradict this real failure.

No source change, alternative module, rebuild, retry, pin replacement, payload
regeneration or scientific invocation followed. No extra account/log RPC was
needed: original launcher logs and cleanup receipt already contain decisive facts.
Next condition, for S0 review only: a separately scoped way to validate how this
fixed builder function's defining module reaches the remote build environment.
Any code change needs a new reviewed source identity and applicable authorization;
this session's attempt allowance is consumed and does not resume itself.

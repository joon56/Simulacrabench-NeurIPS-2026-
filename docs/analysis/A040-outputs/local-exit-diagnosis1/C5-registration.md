# C5 - output-manager wrapper interaction
C4 removing await-chain observation did not alter native failure. Source:
Endpoint._build wraps Image.build with SDK.enable_output, which lazily imports
Rich and constructs a RichOutputManager (installed modal/output.py).
Hypothesis: output-manager interaction is required for the crash.
Single diagnostic change in local Endpoint copy: await the same image.build(app)
without that display wrapper. No SDK patch/guard change or build bypass.
Expected exit0 implicates the wrapper; same crash rejects its necessity.
This is diagnosis, not a production repair or approved output-policy change.
# C6 - builder protobuf response without resolver/build
C5 output wrapper removal also crashed. Official protobuf issue22067 describes
a different-version shutdown-GC failure; similarity is not attribution.
Single addition to clean C3 definition control: construct the fixture's
FunctionCreate response graph and consume it with actual FunctionInfo parser.
No Image.build, mount thread pool, output manager, or await-chain observation.
Prediction: crash would isolate builder-message construction/parsing as a
sufficient trigger; exit0 rejects sufficiency, leaving actual build/resolve
interaction unresolved. c6-protobuf. No backend/version replacement.
This is the sixth and final named comparison. Further work is closeout unless
this comparison supplies cause-based repair within the same boundary.
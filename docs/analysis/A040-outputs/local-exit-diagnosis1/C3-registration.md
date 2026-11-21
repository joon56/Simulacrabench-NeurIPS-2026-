# C3 - image definition versus build
Registered before c3-definition. C2 reduced builder still crashes; Context and
launcher are not required. One changed boundary: stop after run_function image
definition; do not invoke Endpoint._build/Image.build. Keep client/app setup,
same guard/transport, managed loop and AppStop.
Prediction: definition exit0 narrows the trigger to actual build/resolver path;
definition crash would move the first failing boundary earlier.

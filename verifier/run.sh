#!/bin/bash
set -e

mkdir -p /verifier

pytest /tests/test_outputs.py \
  --json-report \
  --ctrf=/verifier/ctrf.json

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo 1 > /verifier/reward.txt
    echo '{"reward":1}' > /verifier/reward.json
else
    echo 0 > /verifier/reward.txt
    echo '{"reward":0}' > /verifier/reward.json
fi

ls -la /verifier

exit 0
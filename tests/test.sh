#!/bin/bash
set -e

mkdir -p /logs/verifier

pytest /tests/test_outputs.py \
    --json-report \
    --ctrf=/logs/verifier/ctrf.json

RESULT=$?

if [ $RESULT -eq 0 ]; then
    REWARD=1
else
    REWARD=0
fi

echo "$REWARD" > /logs/verifier/reward.txt
cat > /logs/verifier/reward.json <<EOF
{
  "reward": $REWARD
}
EOF

echo "Verifier files:"
ls -la /logs/verifier/
cat /logs/verifier/reward.txt

exit 0
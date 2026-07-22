#!/bin/bash
set -e

echo "=== Verifier Started ==="
echo "Files in /app:"
ls -la /app/

mkdir -p /logs/verifier

echo "Running pytest..."
pytest /tests/test_outputs.py -rA
PYTEST_EXIT=$?

if [ $PYTEST_EXIT -eq 0 ]; then
    REWARD=1
else
    REWARD=0
fi

echo "$REWARD" > /logs/verifier/reward.txt
echo "Reward written: $REWARD"

# Create reward.json without heredoc
echo "{\"reward\": $REWARD}" > /logs/verifier/reward.json

echo "=== Verifier files ==="
ls -la /logs/verifier/
cat /logs/verifier/reward.txt

exit 0
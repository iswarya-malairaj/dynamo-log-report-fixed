#!/bin/bash
# Run pytest with the correct Python path
set -e  # Exit on error

echo "Running verifier tests..."
PYTHONPATH=/app python -m pytest /app/tests/test_outputs.py -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Tests failed!"
    exit 1
fi
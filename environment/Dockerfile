FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

# Install required packages
RUN pip install --no-cache-dir \
    numpy==2.1.3 \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

# Create directories
RUN mkdir -p /app /logs/verifier

# Copy task files
COPY . /app/

# Copy access log if it exists
COPY data/access.log /app/access.log 2>/dev/null || true

# Set working directory
WORKDIR /app

# Make test.sh executable
RUN chmod +x /app/tests/test.sh 2>/dev/null || true

# Default command (will be overridden by Harbor)
CMD ["sleep", "infinity"]
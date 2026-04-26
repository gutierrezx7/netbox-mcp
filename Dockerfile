FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY pyproject.toml ./
RUN python -m pip install --upgrade pip
RUN pip install pydantic pydantic-settings httpx

# Copy source
COPY src/ ./src/
COPY README.md ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "netbox_mcp_server"]

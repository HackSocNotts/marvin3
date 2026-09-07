FROM python:3.13-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first for Docker layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Use the virtual environment created by uv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "bot.py"]
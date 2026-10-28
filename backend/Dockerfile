FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /uv/bin/uv
ENV PATH="/uv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY app ./app
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
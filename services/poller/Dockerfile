FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv lock && uv sync --locked
EXPOSE 8000

CMD ["uv", "run", "-m", "src.main"]
FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app

# Copy the project into the image
ADD . /app

# Sync the project
RUN uv sync --frozen --no-install-project

EXPOSE 8501 

CMD [ "uv", "run", "streamlit", "run", "main.py" ]

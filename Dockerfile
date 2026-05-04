# 1. Use an official, lightweight Python image.
FROM python:3.13-slim

# 2. Install the uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Define the working directory
WORKDIR /app

# 4. Create the data directory for SQLite persistence
RUN mkdir -p /app/data

# 5. Copy the dependency files first (optimizes Docker caching)
COPY pyproject.toml uv.lock ./

# 6. Install the dependencies (without creating a venv inside Docker, we use the container system)
RUN uv sync --frozen --no-cache --no-install-project

# 7. Copy the rest of the code
COPY . .

# 8. Expose the port that FastAPI uses
EXPOSE 8000

# 9. Adjust the PYTHONPATH so that Python can finde 'app' package inside 'src'
ENV PYTHONPATH=/app/src

# 10. Command to run the application
# We use /bin/sh -c to allow chaining of commands with '&&'
# Added --app-dir src to ensure uvicorn finds the 'app' package correctly
CMD ["/bin/sh", "-c", "uv run alembic upgrade head && uv run python seed.py && uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --app-dir src"]
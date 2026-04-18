# 1. Use an official, lightweight Python image.
FROM python:3.14-slim

# 2. Install the uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Define the working directory
WORKDIR /app

# 4. Copy the dependency files first (optimizes Docker caching)
COPY pyproject.toml uv.lock ./

# 5. Install the dependencies (without creating a venv inside Docker, we use the container system)
RUN uv sync --frozen --no-cache

# 6. Copy the rest of the code
COPY . .

# 7. Expose the port that FastAPI uses
EXPOSE 8000

# 8. Command to run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Multi-stage Dockerfile for Container Loading Optimizer
# Epic 5 - Docker & Cloud Run Implementation

# Stage 1: Python backend + tests
FROM python:3.12-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/
COPY tests/ ./tests/

# Set Python path
ENV PYTHONPATH=/app

# Stage 2: Node.js frontend build
FROM node:20 as frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 3: Final production image
FROM python:3.12-slim

WORKDIR /app

# Copy Python dependencies from backend-builder
COPY --from=backend-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend application code
COPY --from=backend-builder /app/backend ./backend

# Copy frontend build output to backend static directory
COPY --from=frontend-builder /app/frontend/dist ./backend/static

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080
ENV DATABASE_URL=sqlite:///app.db

# Expose port
EXPOSE 8080

# Run the FastAPI application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

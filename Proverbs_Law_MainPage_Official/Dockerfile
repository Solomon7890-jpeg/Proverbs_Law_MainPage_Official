# Stage 1: Build the 3D Next.js Frontend
FROM node:18-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the 'Ultimate Brain' Backend & Serve
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies for OCR & Voice
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files and the compiled 3D frontend
COPY . .
COPY --from=frontend-builder /app/frontend/out ./frontend-dist

# Production Environment Settings
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Production Entrypoint: Status-Aware Uvicorn Service
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--timeout-keep-alive", "65"]

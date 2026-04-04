FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Ensure environmental output is not buffered
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Production command for Cloud Run (scaling via uvicorn)
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]

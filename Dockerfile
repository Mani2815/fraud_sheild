FROM python:3.10-slim

# Install Tesseract + languages
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Gunicorn entrypoint
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]

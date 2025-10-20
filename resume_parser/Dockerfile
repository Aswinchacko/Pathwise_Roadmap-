FROM python:3.11-slim

LABEL maintainer="PathWise Team"
LABEL description="Resume Parser Service"

# Set working directory
WORKDIR /app

# Install system dependencies for PDF/DOCX parsing
RUN apt-get update && apt-get install -y \
    curl \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8007

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8007/health || exit 1

# Run the application
CMD ["python", "main.py"]


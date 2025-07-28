FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy source code
COPY src/ ./src/

# Create directories for input/output
RUN mkdir -p /app/data /app/output

# Set Python path
ENV PYTHONPATH=/app

# Make main.py executable
RUN chmod +x src/main.py

# Default command
CMD ["python", "src/main.py"]
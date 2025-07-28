# Multi-Collection PDF Analysis System Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PyMuPDF and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
USER app

# Copy source code and scripts (as app user)
COPY --chown=app:app src/ ./src/
COPY --chown=app:app Challenge_1b/ ./Challenge_1b/
COPY --chown=app:app run_challenge.py .
COPY --chown=app:app analyze_compliance.py .
COPY --chown=app:app verify_exact_structure.py .
COPY --chown=app:app validate_docker.py .
COPY --chown=app:app docker_setup.py .
COPY --chown=app:app approach_explanation.md .
COPY --chown=app:app README.md .

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create output directory
RUN mkdir -p /app/output

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, 'src'); from main import MultiCollectionPDFAnalyzer; print('OK')" || exit 1

# Default command - run all challenge collections
CMD ["python", "run_challenge.py"]

# Alternative commands (can be overridden)
# docker run pdf-analysis-system python run_challenge.py 1
# docker run pdf-analysis-system python analyze_compliance.py
# docker run pdf-analysis-system python verify_exact_structure.py

# Labels
LABEL maintainer="PDF Analysis System"
LABEL version="1.0"
LABEL description="Multi-Collection PDF Analysis System for Challenge 1b - Command Line Only"
LABEL org.opencontainers.image.source="https://github.com/your-repo/pdf-analysis-system"
LABEL org.opencontainers.image.documentation="https://github.com/your-repo/pdf-analysis-system/README.md"
# Base image
FROM ghcr.io/railwayapp/nixpacks:ubuntu-1733184274

# Set working directory
WORKDIR /app/

# Copy application files
COPY . /app/.

# Install dependencies, cloud-init, and python3-venv for virtual environment creation
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    cloud-init \
    distro-info \
    language-selector-common && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Start command
CMD ["python", "run.py"]


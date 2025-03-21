
# Base image
FROM ghcr.io/railwayapp/nixpacks:ubuntu-1733184274

# Set working directory
WORKDIR /app/

# Copy application files
COPY . /app/.

# Install dependencies, cloud-init, python3-venv, python-is-python3 for python alias
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    cloud-init \
    distro-info \
    language-selector-common \
    python-is-python3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Set environment path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Start command
CMD ["python", "run.py"]


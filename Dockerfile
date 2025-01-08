# Base image
FROM ghcr.io/railwayapp/nixpacks:ubuntu-1733184274

# Set working directory
WORKDIR /app/

# Copy application files
COPY . /app/.

# Install dependencies, cloud-init, and python3-venv for virtual environment creation
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv cloud-init distro-info language-selector && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set environment path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Start command
CMD ["python", "run.py"]


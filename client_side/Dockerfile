FROM python:3.12.4-slim

# Update package list and install necessary build tools and libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Turn off history file creation (optional)
RUN echo "export HISTFILE=/dev/null" >> /etc/profile

# Add a user (with no password) so we don't run as root:
RUN useradd -m -s /bin/bash user

# Install any additional Python packages we need:
RUN pip3 install --upgrade pip setuptools
RUN pip3 install requests
RUN pip3 install jsons

# Switch to the non-root user:
USER user




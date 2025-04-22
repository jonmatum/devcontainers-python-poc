FROM python:3.12.3-slim-bookworm

WORKDIR /workspace

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    build-essential \
    && pip install --no-cache-dir pipenv \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws/

# Copy app and Pipenv files
COPY . .

# Set PATH to make VS Code happy
ENV PATH="/workspace/.venv/bin:$PATH"
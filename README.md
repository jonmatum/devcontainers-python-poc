# FastAPI Lambda DevContainer

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/github/license/YOUR_GITHUB_USERNAME/devcontainers-python-poc.svg)](LICENSE)
[![Pipenv](https://img.shields.io/badge/pipenv-managed-blueviolet)](https://pipenv.pypa.io/)
[![DevContainer](https://img.shields.io/badge/devcontainer-ready-blue)](https://code.visualstudio.com/docs/devcontainers/containers)

This repository provides a fully configured development environment for building and testing FastAPI applications intended to run on AWS Lambda. The environment uses Docker, VS Code DevContainers, and Pipenv to offer an isolated, reproducible, and developer-friendly workflow.


## Features

- Python 3.12 (via official slim Bookworm base image)
- FastAPI application configured for AWS Lambda via Mangum
- Pre-installed developer tooling: pytest, coverage, mypy, black, isort
- Linting and formatting scripts using Pipenv
- HTML coverage reports via `coverage html`
- DevContainer ready for VS Code Remote - Containers integration
- AWS CLI installed in the container for cloud deployment workflows



## Project Structure

<!-- tree -a --dirsfirst -I '.git|.venv|.vscode|.pytest_cache|.mypy_cache|htmlcov|.DS_Store|.coverage|__pycache__|.coveragerc|.env' . -->

```
.
├── .devcontainer
│   ├── Dockerfile
│   └── devcontainer.json
├── app
│   ├── __init__.py
│   └── main.py
├── tests
│   └── test_main.py
├── Pipfile
├── Pipfile.lock
└── README.md
```



## Application Overview

### FastAPI App (`app/main.py`)

```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda"}

handler = Mangum(app)
```

This setup allows the FastAPI app to run on Lambda using API Gateway via Mangum.



## Development Environment

### DevContainer Configuration

```json
{
  "name": "Python FastAPI Lambda Dev",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "bash",
        "python.pythonPath": "/workspace/.venv/bin/python"
      },
      "extensions": [
        "ms-python.python",
        "ms-azuretools.vscode-docker"
      ]
    }
  },
  "postCreateCommand": "pipenv --python /usr/local/bin/python install --dev",
  "forwardPorts": [8000],
  "remoteUser": "root"
}
```

### Dockerfile Summary

```dockerfile
FROM python:3.12.3-slim-bookworm

WORKDIR /workspace

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PATH="/workspace/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    build-essential \
    && pip install --no-cache-dir pipenv \
    && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws/

COPY . .
```



## Pipenv Setup

### `Pipfile`

```toml
[requires]
python_version = "3.12"

[packages]
fastapi = "*"
uvicorn = { extras = ["standard"] }
mangum = "*"
boto3 = "*"

[dev-packages]
pytest = "*"
black = "*"
isort = "*"
mypy = "*"
httpx = "*"
coverage = "*"

[scripts]
dev = "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
test = "pytest"
format = "black ."
lint = "sh -c 'env PYTHONPATH=. isort . && env PYTHONPATH=. black --check . && env PYTHONPATH=. mypy app'"
coverage = "sh -c 'env PYTHONPATH=. coverage run -m pytest && coverage report -m'"
coverage-html = "sh -c 'env PYTHONPATH=. coverage run -m pytest && coverage html'"
```



## Usage

### Start the DevContainer

1. Open the project in VS Code
2. Select "Reopen in Container"
3. Wait for dependencies to install

### Run the FastAPI Dev Server

```bash
pipenv run dev
```

Access the API at: http://localhost:8000

### Run Tests

```bash
pipenv run test
```

### Lint and Type Check

```bash
pipenv run lint
```

### Format Code

```bash
pipenv run format
```

### Generate Coverage Report

```bash
pipenv run coverage
```

### View Coverage Report (HTML)

```bash
pipenv run coverage-html
# Open htmlcov/index.html in your browser
```



## Testing Example

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI on Lambda"}
```



## Requirements

- Docker
- VS Code + Remote - Containers extension
- No need to install Python or dependencies locally



## Deployment

The app is designed for deployment to AWS Lambda via API Gateway. Use the provided AWS CLI or tools like Serverless Framework, AWS SAM, or Terraform. The Lambda handler is exposed via:

```python
handler = Mangum(app)
```

## License

MIT License
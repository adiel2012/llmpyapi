# DeepSeek LLM Flask API

Welcome to the DeepSeek LLM Flask API project. This application creates a production-ready REST API that makes the powerful DeepSeek language model accessible through HTTP requests. Whether you're developing locally or deploying to production, this guide will help you understand and work with the system effectively.

## Understanding the Project

Let's start by understanding what makes this project work and how its pieces fit together to create a powerful language model service.

### The Model: Our Foundation

At the heart of this project lies the DeepSeek LLM 7B Chat model. This sophisticated language model is designed specifically for conversational interactions, making it ideal for a wide range of applications. We use a quantized version (Q4_K_M) that provides an excellent balance between performance and resource usage.

You can obtain the model file (deepseek-llm-7b-chat.Q4_K_M.gguf) from Hugging Face:
[DeepSeek LLM 7B Chat GGUF Model](https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF/blob/main/deepseek-llm-7b-chat.Q4_K_M.gguf)

The Q4_K_M quantization is particularly important because it reduces the model's memory footprint while maintaining high-quality outputs. This makes it possible to run the model efficiently even in environments with limited resources.

### Project Structure

Our application follows a modular architecture that separates concerns and promotes maintainability. Here's how the components are organized:

```
project/
├── src/                    # Application source code
│   ├── api/               # API layer
│   │   ├── __init__.py
│   │   ├── routes.py     # Route definitions
│   │   └── endpoints.py   # Endpoint implementations
│   ├── config/           # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py   # Application settings
│   ├── utils/            # Utility functions
│   │   ├── __init__.py
│   │   └── model_handler.py  # Model interaction logic
│   └── app.py            # Application entry point
├── models/               # Model storage
├── logs/                # Application logs
├── tests/               # Test suite
├── docker/              # Docker configuration
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── .env                 # Environment variables
├── model-setup.bat      # Model setup script
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

Before starting, ensure you have:
1. Docker Desktop installed and running
2. Python 3.11 or later installed (3.12 is supported)
3. Approximately 8GB of free RAM for model operation
4. At least 5GB of free disk space for the model file

### Model File Management

The first and most crucial step is setting up the model file correctly. Since we're working with Docker, we need a reliable way to give our containers access to this large file. We use Docker volumes for this purpose because they provide several important benefits:

1. The model file remains available even when containers are removed
2. Volumes provide better I/O performance than bind mounts
3. Volumes can be easily shared between different containers
4. The model file can be managed independently of container lifecycle

To set up the model, we use a script called `model-setup.bat`. Create this script in your project root with the following content:

```batch
@echo off
REM This script manages the setup of the model file for Docker containers

echo Starting model setup process...
echo.

REM Create the models directory if it doesn't exist
if not exist models (
    echo Creating models directory...
    mkdir models
    echo Models directory created successfully.
    echo.
)

REM Check if the model file exists in the models directory
if not exist models\deepseek-llm-7b-chat.Q4_K_M.gguf (
    echo Model file not found in models directory.
    echo.
    echo Please perform the following steps:
    echo 1. Download deepseek-llm-7b-chat.Q4_K_M.gguf from:
    echo    https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF/blob/main/deepseek-llm-7b-chat.Q4_K_M.gguf
    echo 2. Place the file in the 'models' directory
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Model file found in models directory.
echo.

REM Create Docker volume if it doesn't exist
echo Checking Docker volume...
docker volume inspect model_storage >nul 2>&1
if errorlevel 1 (
    echo Creating Docker volume 'model_storage'...
    docker volume create model_storage
) else (
    echo Docker volume 'model_storage' already exists.
)
echo.

REM Copy model to Docker volume using a temporary container
echo Copying model file to Docker volume...
echo This may take a few minutes depending on the file size...
docker run --rm -v model_storage:/data -v "%cd%/models":/source alpine sh -c "cp /source/deepseek-llm-7b-chat.Q4_K_M.gguf /data/"

if errorlevel 1 (
    echo.
    echo Error: Failed to copy model file to Docker volume.
    echo Please ensure Docker is running and try again.
    pause
    exit /b 1
)

echo.
echo Model setup completed successfully!
echo The model is now ready to be used by Docker containers.
echo.
echo You can now run the application using:
echo - For development: .\run-docker-dev.bat
echo - For production: .\run-docker-prod.bat
echo.
pause
```

After creating the script:
1. Download the model file and place it in the `models` directory
2. Run the setup script:
```bash
.\model-setup.bat
```

### Environment Configuration

Create a `.env` file in your project root with these settings:

```ini
MODEL_PATH=/app/models/deepseek-llm-7b-chat.Q4_K_M.gguf
MAX_TOKENS=4096
CONTEXT_LENGTH=4096
DEFAULT_TEMPERATURE=0.7
```

## Docker Development Environment

The development environment is designed for active development with features like hot-reloading and mounted volumes. Here are the essential commands:

### Starting Development Environment

```bash
# Build and start containers
docker-compose up --build

# Or use the convenience script
.\run-docker-dev.bat
```

### Development Commands

Viewing Logs:
```bash
# View continuous log output
docker-compose logs -f

# View specific service logs
docker-compose logs api
```

Container Access:
```bash
# Access a shell in the container
docker-compose exec api bash

# Run tests inside the container
docker-compose exec api pytest
```

Managing the Environment:
```bash
# Stop containers while preserving data
docker-compose stop

# Remove containers but keep volumes
docker-compose down

# Complete cleanup including volumes
docker-compose down -v
```

## Docker Production Environment

The production environment is optimized for performance and reliability, using Gunicorn as the WSGI server. Here are the key commands:

### Starting Production Environment

```bash
# Build and start production environment
docker-compose -f docker-compose.prod.yml up --build -d

# Or use the production script
.\run-docker-prod.bat
```

### Production Commands

Monitoring:
```bash
# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Check container health
docker-compose -f docker-compose.prod.yml ps

# Monitor resource usage
docker stats
```

Scaling:
```bash
# Scale the API service
docker-compose -f docker-compose.prod.yml up -d --scale api=3
```

## Using the API

The service provides two main endpoints:

### Health Check
```http
GET /health
```

Response:
```json
{
    "status": "healthy",
    "model": "models/deepseek-llm-7b-chat.Q4_K_M.gguf"
}
```

### Text Generation
```http
POST /generate
Content-Type: application/json

{
    "prompt": "Your prompt text here",
    "max_tokens": 1024
}
```

Example using curl:
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms", "max_tokens": 1024}'
```

## Performance Optimization

Several factors affect the model's performance:

### Memory Usage
- The model requires approximately 8GB of RAM
- Docker configurations include memory limits
- Monitor memory usage in production environments

### CPU/GPU Utilization
- CPU threads are automatically configured
- GPU acceleration can be enabled by modifying `n_gpu_layers`
- Monitor CPU usage and adjust worker count based on load

### Response Times
- Context length significantly affects processing time
- Consider batching requests when possible
- Choose appropriate `max_tokens` values for your use case

## Troubleshooting Guide

If you encounter issues, follow these troubleshooting steps:

### Model Access Issues
```bash
# Verify model in Docker volume
docker run --rm -v model_storage:/data alpine ls -l /data

# Check model path in container
docker-compose exec api ls -l /app/models

# Verify environment variables
docker-compose exec api env | grep MODEL_PATH
```

### Performance Issues
```bash
# Check container resources
docker stats

# View application logs
docker-compose logs -f api

# Monitor CPU usage
docker-compose top api
```

### Container Issues
```bash
# Check container status
docker-compose ps

# Inspect container configuration
docker inspect api

# View startup logs
docker-compose logs --tail=50 api
```

## Security Considerations

The API implements several security measures:

### Input Validation
- Request size limits prevent memory exhaustion
- Content type verification ensures proper data handling
- Parameter validation protects against invalid inputs

### Resource Protection
- Rate limiting prevents API abuse
- Memory usage limits protect system resources
- Worker timeout configuration prevents hung processes

### Error Handling
- Sanitized error messages prevent information leakage
- Proper HTTP status codes indicate error types
- Comprehensive logging tracks security events

## Contributing

We welcome contributions to improve the project. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please include:
- Tests for new features
- Documentation updates
- Clear commit messages
- Description of changes in PR

## License

This project is open source and available under the MIT License. The DeepSeek LLM model has its own license terms - please refer to the [Hugging Face model page](https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF) for details.
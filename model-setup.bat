@echo off
REM This script manages the setup of the model file for Docker containers
REM It creates necessary directories, checks for the model file, and sets up Docker volumes

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
# DeepSeek LLM Flask API

This project provides a Flask-based REST API for interacting with the DeepSeek LLM model. It allows you to make queries to the model through HTTP endpoints, making it easy to integrate the model's capabilities into various applications.

## Model Information

This implementation uses the DeepSeek LLM 7B Chat model, which is optimized for conversational interactions. The model file (deepseek-llm-7b-chat.Q4_K_M.gguf) can be downloaded from Hugging Face:

[DeepSeek LLM 7B Chat GGUF Model](https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF/blob/main/deepseek-llm-7b-chat.Q4_K_M.gguf)

The model is quantized using Q4_K_M quantization, offering a good balance between performance and resource usage.

## Project Structure

The project follows a modular structure for better organization and maintainability:

```
project/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── endpoints.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── model_handler.py
│   └── app.py
├── models/
├── logs/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Installation

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the model and place it in the `models` directory, or update the MODEL_PATH in your `.env` file to point to your model location.

## Configuration

Create a `.env` file in the project root with the following settings:

```ini
MODEL_PATH=models/deepseek-llm-7b-chat.Q4_K_M.gguf
MAX_TOKENS=4096
CONTEXT_LENGTH=4096
DEFAULT_TEMPERATURE=0.7
```

Adjust these values according to your needs and available resources.

## Running the Application

To start the API server:

```bash
python src/app.py
```

The server will start on `http://localhost:5000` by default.

## API Endpoints

### Health Check
```bash
GET /health
```
Returns the status of the service and model information.

### Generate Response
```bash
POST /generate
Content-Type: application/json

{
    "prompt": "Your prompt here",
    "max_tokens": 1024
}
```

Example curl command:
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me a short story about a robot learning to paint", "max_tokens": 1024}'
```

## Development Notes

### Debugging in VS Code

The project includes a VS Code launch configuration for debugging. To use it:

1. Open the project in VS Code
2. Set breakpoints in your code
3. Press F5 or select "Flask: Debug API" from the debug configurations
4. The debugger will stop at your breakpoints

### Model Performance

The DeepSeek LLM 7B Chat model requires approximately 8GB of RAM. Performance can be improved by:
- Enabling GPU acceleration by setting `n_gpu_layers` in the model configuration
- Adjusting the number of threads based on your CPU capabilities
- Fine-tuning the context length and max tokens based on your use case

## Error Handling

The API includes comprehensive error handling for common scenarios:
- Missing model file
- Invalid requests
- Model generation errors
- Resource constraints

All errors are logged and return appropriate HTTP status codes with descriptive messages.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions for improvements.

## License

This project is open source. The DeepSeek LLM model is subject to its own license terms - please refer to the [Hugging Face model page](https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF) for details.
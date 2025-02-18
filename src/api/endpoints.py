from flask import request, jsonify
from utils.model_handler import ModelHandler
from config.settings import get_settings

model_handler = None

def register_endpoints(app):
    global model_handler
    settings = get_settings()
    model_handler = ModelHandler(settings.MODEL_PATH)

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy", "model": settings.MODEL_PATH})

    @app.route("/generate", methods=["POST"])
    def generate():
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        data = request.get_json()
        if "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' field in request"}), 400
        response = model_handler.generate_response(
            data["prompt"], 
            max_tokens=data.get("max_tokens", 512)
        )
        return jsonify(response)

# src/config/settings.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

@dataclass
class Settings:
    MODEL_PATH: str
    MAX_TOKENS: int = 4096  # Increased for 7B model
    DEFAULT_TEMPERATURE: float = 0.7
    CONTEXT_LENGTH: int = 4096  # Added for 7B model

    def validate(self):
        """Validate settings and provide helpful error messages."""
        if not os.path.exists(self.MODEL_PATH):
            actual_path = os.path.abspath(self.MODEL_PATH)
            logger.error(f"Model file not found at: {actual_path}")
            logger.error("Please ensure the model file exists and the path is correct in your .env file")
            raise ValueError(
                f"Model file not found. Expected at: {actual_path}\n"
                "Please either:\n"
                "1. Place the deepseek-llm-7b-chat.Q4_K_M.gguf file in the 'models' directory, or\n"
                "2. Update MODEL_PATH in .env to point to your model file location"
            )

def get_settings() -> Settings:
    """Get and validate application settings."""
    load_dotenv()
    
    # Default to looking in a models subdirectory
    default_model_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'models',
        'deepseek-llm-7b-chat.Q4_K_M.gguf'
    )
    
    settings = Settings(
        MODEL_PATH=os.getenv('MODEL_PATH', default_model_path),
        MAX_TOKENS=int(os.getenv('MAX_TOKENS', '4096')),
        DEFAULT_TEMPERATURE=float(os.getenv('DEFAULT_TEMPERATURE', '0.7')),
        CONTEXT_LENGTH=int(os.getenv('CONTEXT_LENGTH', '4096'))
    )
    
    settings.validate()
    return settings
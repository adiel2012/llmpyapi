from llama_cpp import Llama
import os
import logging

logger = logging.getLogger(__name__)

class ModelHandler:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.llm = self._load_model()
    
    def _load_model(self):
        try:
            return Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=os.cpu_count(),
                n_gpu_layers=0
            )
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 512):
        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
                stop=["</s>", "\n\n"],
                echo=False
            )
            
            return {
                "generated_text": output["choices"][0]["text"],
                "tokens_used": output["usage"]["total_tokens"],
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }
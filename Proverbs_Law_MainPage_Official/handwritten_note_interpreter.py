# handwritten_note_interpreter.py

from typing import Dict, List, Any, Optional
from huggingface_hub import InferenceClient
import pytesseract
from PIL import Image
import io
import base64

# Tesseract-OCR needs to be installed and its path added to PATH or specified here
# pytesseract.pytesseract.tesseract_cmd = r'C:\ Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows

class HandwrittenNoteInterpreter:
    """
    Enhanced Handwriting Interpreter with Vision-AI.
    Analyzes penmanship and extracts legal data from images/PDFs.
    """
    def __init__(self, hf_token: str = None, vision_model: str = "meta-llama/Llama-3.2-11B-Vision-Instruct"):
        self.client = InferenceClient(token=hf_token, model=vision_model)
        self.vision_model = vision_model

    def _call_vision_llm(self, image_base64: str, prompt: str) -> str:
        """Helper to call Vision-LLM with an image."""
        try:
            # Construct multi-modal message
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ]
            
            response = ""
            for chunk in self.client.chat_completion(
                messages, 
                max_tokens=2048, 
                stream=True
            ):
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
            return response
        except Exception as e:
            return f"Vision-AI Error: {str(e)}"

    def analyze_penmanship(self, image_base64: str) -> str:
        """
        Learns and analyzes the penmanship style (pinmanship).
        """
        prompt = (
            "Analyze the penmanship in this image. Focus on: "
            "1. Writing style (cursive, print, hybrid) "
            "2. Slant, pressure, and letter formation "
            "3. Consistency and readability "
            "4. Unique characteristics that identifying the 'hand' of the writer. "
            "Provide a detailed psychological and structural analysis of the handwriting."
        )
        return self._call_vision_llm(image_base64, prompt)

    def process_handwritten_note(self, image_path: str) -> Dict[str, Any]:
        """
        Process handwriting: Transcription + Penmanship Analysis + Summary.
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

        transcription_prompt = (
            "Carefully transcribe all handwritten text in this image accurately. "
            "If parts are illegible, use [?] or [illegible]. Maintain the layout."
        )
        
        transcription = self._call_vision_llm(image_base64, transcription_prompt)
        penmanship = self.analyze_penmanship(image_base64)
        
        summary_prompt = f"Summarize the following legal note transciption: \n\n{transcription}"
        # We can use the same vision model for text-only summary or a text-only model
        summary = self._call_vision_llm(image_base64, "Provide a legal summary of the text you just transcribed.")

        return {
            "transcription": transcription,
            "penmanship_analysis": penmanship,
            "legal_summary": summary,
            "model_used": self.vision_model
        }

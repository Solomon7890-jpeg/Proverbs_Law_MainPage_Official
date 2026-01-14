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
    def __init__(self, hf_token: str = None, llm_model: str = "meta-llama/Llama-3.3-70B-Instruct", case_manager_instance=None):
        self.client = InferenceClient(token=hf_token, model=llm_model)
        self.llm_model = llm_model
        self.case_manager = case_manager_instance # Instance of CaseManager to interact with

    def _call_llm(self, messages: List[Dict[str, str]], max_tokens: int = 1024, temperature: float = 0.7, top_p: float = 0.95) -> str:
        """Helper to call the underlying LLM."""
        response_text = ""
        try:
            for message_chunk in self.client.chat_completion(
                messages,
                max_tokens=max_tokens,
                stream=True,
                temperature=temperature,
                top_p=top_p,
            ):
                if message_chunk.choices and message_chunk.choices[0].delta.content:
                    response_text += message_chunk.choices[0].delta.content
            return response_text
        except Exception as e:
            return f"LLM Error: {str(e)}"

    def _ocr_image(self, image_input: Any) -> str:
        """
        Performs OCR on an image.
        image_input can be a file path, a PIL Image object, or base64 encoded string.
        """
        if isinstance(image_input, str):
            if image_input.startswith("data:image"): # Base64 string
                header, encoded = image_input.split(",", 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
            else: # Assume file path
                image = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            raise ValueError("Unsupported image input type. Must be path, PIL Image, or base64 string.")

        try:
            # Ensure Tesseract-OCR is installed and configured
            text = pytesseract.image_to_string(image)
            return text
        except pytesseract.TesseractNotFoundError:
            return "OCR Error: Tesseract-OCR is not installed or not in your PATH. Please install it."
        except Exception as e:
            return f"OCR Error: {str(e)}"

    def summarize_text(self, text: str, case_context: str = "") -> str:
        """
        Summarizes the extracted text using an LLM.
        """
        system_prompt = (
            "You are an AI assistant specialized in summarizing legal notes and documents. "
            "Provide a concise and accurate summary of the following text, "
            "keeping in mind any provided case context."
        )
        user_message = f"Text to summarize:\n\n{text}\n\nCase context: {case_context}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        return self._call_llm(messages)

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extracts key terms from the text using an LLM.
        """
        system_prompt = (
            "You are an AI assistant specialized in extracting keywords from legal text. "
            "Identify and list the most important keywords and phrases from the following text. "
            "Return them as a comma-separated list."
        )
        user_message = f"Text to extract keywords from:\n\n{text}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        keywords_str = self._call_llm(messages)
        return [kw.strip() for kw in keywords_str.split(',') if kw.strip()]

    def process_handwritten_note(self, image_input: Any, case_id: Optional[int] = None, context: str = "") -> Dict[str, Any]:
        """
        End-to-end processing of a handwritten note image.
        Performs OCR, summarizes, extracts keywords, and optionally integrates with a case.
        """
        extracted_text = self._ocr_image(image_input)
        if "OCR Error" in extracted_text:
            return {"error": extracted_text}
        
        summary = self.summarize_text(extracted_text, context)
        keywords = self.extract_keywords(extracted_text)
        
        result = {
            "extracted_text": extracted_text,
            "summary": summary,
            "keywords": keywords,
            "case_integration_status": "No case provided"
        }

        if case_id and self.case_manager:
            note_content = f"Handwritten Note Summary:\n{summary}\n\nFull Extracted Text:\n{extracted_text}"
            added_note = self.case_manager.add_note_to_case(case_id, note_content)
            if added_note:
                result["case_integration_status"] = f"Note added to case {case_id} (Note ID: {added_note['note_id']})"
            else:
                result["case_integration_status"] = f"Failed to add note to case {case_id}."
        
        return result

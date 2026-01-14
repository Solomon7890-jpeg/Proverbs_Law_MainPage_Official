# legal_document_generator.py

from typing import Dict, List, Any
from huggingface_hub import InferenceClient

class LegalDocumentGenerator:
    def __init__(self, hf_token: str = None, llm_model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        self.client = InferenceClient(token=hf_token, model=llm_model)
        self.llm_model = llm_model

    def _call_llm(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7, top_p: float = 0.95) -> str:
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
            return f"LLM Error during document generation: {str(e)}"

    def generate_document(self, document_type: str, user_inputs: Dict[str, str], context: str = "") -> str:
        """
        Generates a legal document based on type and user-provided inputs.

        Args:
            document_type (str): The type of legal document to generate (e.g., "will", "contract", "motion").
            user_inputs (Dict[str, str]): A dictionary of key-value pairs representing user inputs
                                          (e.g., {"client_name": "John Doe", "date": "2023-10-26"}).
            context (str): Additional context or instructions from the SuperLawAgent.

        Returns:
            str: The generated legal document.
        """
        system_prompt = self._get_document_generation_prompt(document_type)
        
        # Construct the user message with all inputs
        input_details = "\n".join([f"- {key}: {value}" for key, value in user_inputs.items()])
        user_message_content = (
            f"Generate a {document_type} using the following information:\n\n"
            f"{input_details}\n\n"
            f"Additional context: {context}\n\n"
            "Ensure the document is professional, legally sound (to the best of AI's ability), and well-formatted."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message_content}
        ]
        
        # Max tokens for document generation might need to be higher
        return self._call_llm(messages, max_tokens=4096, temperature=0.5, top_p=0.9)

    def _get_document_generation_prompt(self, document_type: str) -> str:
        """
        Returns a specialized system prompt for generating a specific type of legal document.
        """
        base_prompt = (
            "You are an AI specialized in drafting legal documents. Your output must be a well-structured, "
            "professional legal document. Do not include conversational text or explanations outside the document itself. "
            "Focus solely on generating the document content."
        )

        prompts = {
            "will": (
                f"{base_prompt}\n\n"
                "Draft a Last Will and Testament. Include standard clauses for executor appointment, "
                "beneficiaries, distribution of assets, guardianship for minors (if applicable), "
                "and residuary estate. Use clear and unambiguous language. "
                "Ensure placeholders for names, dates, and specific bequests."
            ),
            "contract": (
                f"{base_prompt}\n\n"
                "Draft a general contract. Include standard sections like parties involved, "
                "recitals, terms and conditions, obligations, duration, termination clauses, "
                "governing law, and signatures. Adapt to the specific nature implied by user inputs."
            ),
            "motion": (
                f"{base_prompt}\n\n"
                "Draft a legal motion. Include standard formatting: court name, case caption, "
                "title of motion, factual background, legal arguments, and prayer for relief. "
                "Focus on clarity and persuasiveness based on provided details."
            ),
            "pleading": (
                f"{base_prompt}\n\n"
                "Draft a legal pleading (e.g., complaint, answer). Include court name, "
                "case caption, parties, factual allegations, causes of action, and prayer for relief. "
                "Adhere to typical pleading structure."
            ),
            # Add more document types here
        }
        return prompts.get(document_type.lower(), f"{base_prompt}\n\nDraft a legal document of type: {document_type}. Adapt based on the provided inputs.")

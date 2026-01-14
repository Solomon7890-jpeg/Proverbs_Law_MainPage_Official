# agent_orchestrator.py

from typing import Dict, List, Any
from huggingface_hub import InferenceClient
import json
from legal_document_generator import LegalDocumentGenerator
from case_management_module import CaseManager
from handwritten_note_interpreter import HandwrittenNoteInterpreter

class SuperLawAgent:
    def __init__(self, hf_token: str = None, llm_model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        self.client = InferenceClient(token=hf_token, model=llm_model)
        self.llm_model = llm_model
        # Initialize other sub-agents/tools here (e.g., LegalDocumentGenerator, LegalResearcher)
        self.legal_document_generator = LegalDocumentGenerator(hf_token=hf_token, llm_model=llm_model)
        self.legal_research_tool = None # To be implemented
        self.case_manager = CaseManager() # Default db_path will be 'case_files.db'
        self.handwritten_note_interpreter = HandwrittenNoteInterpreter(hf_token=hf_token, llm_model=llm_model, case_manager_instance=self.case_manager)
        # ... other specialized tools as needed

    def _call_llm(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> str:
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

    def _task_decompose_and_plan(self, query: str, chat_history: List[List[str]]) -> List[Dict[str, Any]]:
        """
        Decomposes a complex legal query into smaller, manageable sub-tasks
        and plans the execution flow.
        """
        # This will involve an LLM call or rule-based logic to determine steps
        # For now, it's a placeholder.
        system_prompt = (
            "You are a task decomposition expert. Given a user's legal query and chat history, "
            "break it down into actionable steps and identify necessary tools/sub-agents. "
            "Output as a JSON list of tasks, e.g., [{'task': 'identify_intent', 'args': {'query': ...}}, {'task': 'call_tool', 'tool_name': 'legal_document_generator', 'args': {'doc_type': 'will', ...}}]"
        )
        messages = [{"role": "system", "content": system_prompt}]
        for user_msg, assistant_msg in chat_history:
            if user_msg: messages.append({"role": "user", "content": user_msg})
            if assistant_msg: messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": f"Decompose the following legal query: {query}"})

        # Placeholder for actual LLM call and parsing
        plan_json_str = self._call_llm(messages, max_tokens=500, temperature=0.3, top_p=0.9)
        try:
            # Attempt to parse as JSON. If it fails, treat as simple text response.
            return json.loads(plan_json_str)
        except json.JSONDecodeError:
            return [{"task": "direct_llm_response", "args": {"query": query, "raw_llm_output": plan_json_str}}]


    def _execute_task(self, task_instruction: Dict[str, Any], chat_history: List[List[str]], user_query: str, max_tokens: int, temperature: float, top_p: float) -> str:
        """Executes a single task based on the decomposed plan."""
        task_type = task_instruction.get("task")
        task_args = task_instruction.get("args", {})

        if task_type == "direct_llm_response":
            # Fallback or simple response
            if "raw_llm_output" in task_args:
                return task_args["raw_llm_output"] # Use pre-generated LLM output if available
            else:
                messages = [{"role": "system", "content": "You are a helpful legal assistant."}] # Default system prompt
                for user_msg, assistant_msg in chat_history:
                    if user_msg: messages.append({"role": "user", "content": user_msg})
                    if assistant_msg: messages.append({"role": "assistant", "content": assistant_msg})
                messages.append({"role": "user", "content": user_query}) # Use original query for direct response
                return self._call_llm(messages, max_tokens, temperature, top_p)

        elif task_type == "call_tool":
            tool_name = task_args.get("tool_name")
            if tool_name == "legal_document_generator" and self.legal_document_generator:
                document_type = task_args.get("document_type")
                user_inputs = task_args.get("user_inputs", {})
                context = task_args.get("context", "")
                return self.legal_document_generator.generate_document(document_type, user_inputs, context)
            elif tool_name == "case_manager" and self.case_manager:
                action = task_args.get("action")
                if action == "create_case":
                    title = task_args.get("title")
                    description = task_args.get("description", "")
                    status = task_args.get("status", "Open")
                    return self.case_manager.create_case(title, description, status)
                elif action == "get_case":
                    case_id = task_args.get("case_id")
                    return self.case_manager.get_case(case_id)
                elif action == "list_cases":
                    status = task_args.get("status")
                    return self.case_manager.list_cases(status)
                elif action == "add_note_to_case":
                    case_id = task_args.get("case_id")
                    content = task_args.get("content")
                    return self.case_manager.add_note_to_case(case_id, content)
                elif action == "get_notes_for_case":
                    case_id = task_args.get("case_id")
                    return self.case_manager.get_notes_for_case(case_id)
                elif action == "add_document_to_case":
                    case_id = task_args.get("case_id")
                    title = task_args.get("title")
                    file_path = task_args.get("file_path")
                    return self.case_manager.add_document_to_case(case_id, title, file_path)
                elif action == "get_documents_for_case":
                    case_id = task_args.get("case_id")
                    return self.case_manager.get_documents_for_case(case_id)
                elif action == "update_case":
                    case_id = task_args.get("case_id")
                    title = task_args.get("title")
                    description = task_args.get("description")
                    status = task_args.get("status")
                    return self.case_manager.update_case(case_id, title, description, status)
                elif action == "delete_case":
                    case_id = task_args.get("case_id")
                    return self.case_manager.delete_case(case_id)
                return f"CaseManager action '{action}' not recognized."
            elif tool_name == "handwritten_note_interpreter" and self.handwritten_note_interpreter:
                image_input = task_args.get("image_input")
                case_id = task_args.get("case_id")
                context = task_args.get("context", "")
                return self.handwritten_note_interpreter.process_handwritten_note(image_input, case_id, context)
            # Add more tool calls here
            return f"Tool '{tool_name}' not yet implemented or available."
        
        elif task_type == "dual_analysis":
            # This is where the core "Dual Analysis" logic would be invoked
            # It would likely call the LLM twice with different system prompts or perspectives
            # For now, it's a placeholder.
            analysis_result_1 = self._perform_analysis_perspective_1(user_query, chat_history, max_tokens, temperature, top_p)
            analysis_result_2 = self._perform_analysis_perspective_2(user_query, chat_history, max_tokens, temperature, top_p)
            return self._format_dual_analysis_output(analysis_result_1, analysis_result_2)

        # ... other task types (e.g., database interaction, external API calls)

        return f"Unknown task type: {task_type}"
    
    def _perform_analysis_perspective_1(self, query: str, chat_history: List[List[str]], max_tokens: int, temperature: float, top_p: float) -> str:
        """Performs analysis from the 'lawful' perspective."""
        system_prompt = (
            "You are a highly analytical Legal Expert specializing in the **Lawful Perspective**. "
            "Your task is to analyze the user's legal query exclusively through the lens of: "
            "1.  **Natural Law:** Universal moral principles, inherent justice, rights endowed by creator/nature. "
            "2.  **Common Law:** Historical judicial precedents, established customs, and unwritten laws. "
            "3.  **Inherent Rights:** Fundamental, inalienable rights of individuals. "
            "Focus on the underlying principles, maxims, and jurisprudential foundations. "
            "Provide a clear, concise, and objective analysis, avoiding statutory jargon where possible, "
            "and emphasizing the ethical and foundational aspects of the matter. "
            "Structure your response to clearly articulate the lawful position, its implications, and any relevant historical context."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for user_msg, assistant_msg in chat_history:
            if user_msg: messages.append({"role": "user", "content": user_msg})
            if assistant_msg: messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": query})
        return self._call_llm(messages, max_tokens, temperature, top_p)

    def _perform_analysis_perspective_2(self, query: str, chat_history: List[List[str]], max_tokens: int, temperature: float, top_p: float) -> str:
        """Performs analysis from the 'legal' perspective."""
        system_prompt = (
            "You are a highly analytical Legal Expert specializing in the **Legal (Statutory) Perspective**. "
            "Your task is to analyze the user's legal query exclusively through the lens of: "
            "1.  **Statutory Law:** Enacted legislation, codes, and acts passed by legislative bodies. "
            "2.  **Regulations:** Rules and administrative codes issued by governmental agencies. "
            "3.  **Binding Legal Precedents:** Decisions from higher courts that lower courts must follow. "
            "Focus on the black-letter law, jurisdictional rules, procedural requirements, and practical application "
            "within existing legal frameworks. Provide a clear, concise, and objective analysis, "
            "citing specific legal provisions or types of statutes where appropriate, "
            "and emphasizing the procedural and enforceable aspects of the matter within the 'legal' system. "
            "Structure your response to clearly articulate the legal position, its requirements, and potential outcomes under current law."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for user_msg, assistant_msg in chat_history:
            if user_msg: messages.append({"role": "user", "content": user_msg})
            if assistant_msg: messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": query})
        return self._call_llm(messages, max_tokens, temperature, top_p)
        
    def _format_dual_analysis_output(self, analysis_1: str, analysis_2: str) -> str:
        """Formats the output to clearly present both lawful and legal perspectives."""
        return (
            "## ⚖️ Dual Analysis Output: Lawful vs. Legal\n\n"
            "--- \n\n"
            "### 🌟 Lawful Perspective (Natural Law, Common Law, Inherent Rights):\n"
            f"{analysis_1}\n\n"
            "--- \n\n"
            "### 📜 Legal/Statutory Perspective (Enacted Laws, Regulations, Precedents):\n"
            f"{analysis_2}\n\n"
            "--- \n\n"
            "This dual analysis provides a comprehensive understanding of the matter from both foundational and enacted legal viewpoints."
        )


    def process_query(self, query: str, chat_history: List[List[str]], mode: str, max_tokens: int, temperature: float, top_p: float) -> str:
        """
        Main entry point for the Super Law Agent to process a user query.
        Orchestrates task decomposition, tool use, and dual analysis.
        """
        # Initially, we can have simple logic: if 'mode' is "dual_analysis", trigger it directly.
        # Otherwise, try to decompose or directly respond.

        if mode == "general_legal_ai_agent": # A new mode for the Super Law Agent
            # Orchestrate task decomposition and execution
            plan = self._task_decompose_and_plan(query, chat_history)
            
            final_output = []
            for task_instruction in plan:
                result = self._execute_task(task_instruction, chat_history, query, max_tokens, temperature, top_p)
                final_output.append(result)
            
            return "\n\n".join(final_output)

        elif mode == "dual_analysis_mode": # A specific mode for dual analysis
            analysis_1 = self._perform_analysis_perspective_1(query, chat_history, max_tokens, temperature, top_p)
            analysis_2 = self._perform_analysis_perspective_2(query, chat_history, max_tokens, temperature, top_p)
            return self._format_dual_analysis_output(analysis_1, analysis_2)

        # Fallback to current simple LLM call for other modes in AILegalChatbotIntegration
        # This part will eventually be replaced by more intelligent orchestration
        messages = [{"role": "system", "content": "You are a helpful legal assistant."}] # Placeholder
        for user_msg, assistant_msg in chat_history:
            if user_msg: messages.append({"role": "user", "content": user_msg})
            if assistant_msg: messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": query})
        return self._call_llm(messages, max_tokens, temperature, top_p)

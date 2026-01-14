# case_management_module.py

from typing import List, Dict, Any, Optional
from datetime import datetime
from database_manager import DatabaseManager

class CaseManager:
    def __init__(self, db_name: str = "proverbs_legal_ai.db"):
        self.db_manager = DatabaseManager(db_name=db_name)

    def create_case(self, title: str, description: str = "", status: str = "Open") -> Optional[Dict[str, Any]]:
        now = datetime.now().isoformat()
        try:
            case_id = self.db_manager.execute_non_query(
                "INSERT INTO cases (title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (title, description, status, now, now)
            )
            return self.get_case(case_id)
        except Exception as e:
            print(f"Error creating case: {e}")
            return None

    def get_case(self, case_id: int) -> Optional[Dict[str, Any]]:
        result = self.db_manager.execute_query("SELECT * FROM cases WHERE case_id = ?", (case_id,))
        if result:
            return result[0] # execute_query returns list of dicts
        return None
    
    def list_cases(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return self.db_manager.execute_query("SELECT * FROM cases WHERE status = ?", (status,))
        else:
            return self.db_manager.execute_query("SELECT * FROM cases")

    def update_case(self, case_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None) -> bool:
        now = datetime.now().isoformat()
        updates = []
        params = []
        if title:
            updates.append("title = ?")
            params.append(title)
        if description:
            updates.append("description = ?")
            params.append(description)
        if status:
            updates.append("status = ?")
            params.append(status)
        
        if not updates:
            return False

        updates.append("updated_at = ?")
        params.append(now)
        params.append(case_id)

        try:
            rows_affected = self.db_manager.execute_non_query(
                f"UPDATE cases SET {', '.join(updates)} WHERE case_id = ?", tuple(params)
            )
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating case {case_id}: {e}")
            return False

    def delete_case(self, case_id: int) -> bool:
        try:
            rows_affected = self.db_manager.execute_non_query("DELETE FROM cases WHERE case_id = ?", (case_id,))
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting case {case_id}: {e}")
            return False

    def add_note_to_case(self, case_id: int, content: str) -> Optional[Dict[str, Any]]:
        now = datetime.now().isoformat()
        try:
            note_id = self.db_manager.execute_non_query(
                "INSERT INTO case_notes (case_id, content, created_at) VALUES (?, ?, ?)",
                (case_id, content, now)
            )
            if note_id:
                result = self.db_manager.execute_query("SELECT * FROM case_notes WHERE note_id = ?", (note_id,))
                if result:
                    return result[0]
            return None
        except Exception as e:
            print(f"Error adding note to case {case_id}: {e}")
            return None
            
    def get_notes_for_case(self, case_id: int) -> List[Dict[str, Any]]:
        return self.db_manager.execute_query("SELECT * FROM case_notes WHERE case_id = ?", (case_id,))

    def add_document_to_case(self, case_id: int, title: str, file_path: str = None) -> Optional[Dict[str, Any]]:
        now = datetime.now().isoformat()
        try:
            doc_id = self.db_manager.execute_non_query(
                "INSERT INTO case_documents (case_id, title, file_path, uploaded_at) VALUES (?, ?, ?, ?)",
                (case_id, title, file_path, now)
            )
            if doc_id:
                result = self.db_manager.execute_query("SELECT * FROM case_documents WHERE document_id = ?", (doc_id,))
                if result:
                    return result[0]
            return None
        except Exception as e:
            print(f"Error adding document to case {case_id}: {e}")
            return None

    def get_documents_for_case(self, case_id: int) -> List[Dict[str, Any]]:
        return self.db_manager.execute_query("SELECT * FROM case_documents WHERE case_id = ?", (case_id,))

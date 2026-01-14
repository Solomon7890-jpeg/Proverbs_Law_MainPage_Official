# database_manager.py

import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name: str = "proverbs_legal_ai.db"):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database and creates tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Cases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'Open',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            # Case Notes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS case_notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
                )
            """)
            # Case Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS case_documents (
                    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    file_path TEXT, -- Storing file path or reference
                    uploaded_at TEXT NOT NULL,
                    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def _get_connection(self):
        """Returns a database connection."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Any]]:
        """Executes a read query and returns results."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row # Allows accessing columns by name
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_non_query(self, query: str, params: tuple = ()) -> int:
        """Executes a write query (INSERT, UPDATE, DELETE) and returns lastrowid or rowcount."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if query.strip().upper().startswith("INSERT"):
                return cursor.lastrowid
            return cursor.rowcount

import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "agent_chat_history.sqlite3"
)


def initialize_chat_history(database_path: Path = DATABASE_PATH) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS chat_messages_conversation_idx
            ON chat_messages (conversation_id, id)
            """
        )


def load_chat_messages(
    conversation_id: str,
    database_path: Path = DATABASE_PATH,
) -> list[dict[str, str]]:
    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,),
        ).fetchall()
    return [{"role": role, "content": content} for role, content in rows]


def save_chat_message(
    conversation_id: str,
    role: str,
    content: str,
    database_path: Path = DATABASE_PATH,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO chat_messages (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )


def clear_chat_history(database_path: Path = DATABASE_PATH) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute("DELETE FROM chat_messages")

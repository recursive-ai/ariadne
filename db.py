import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("ariadne.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, created_at TEXT)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER,
                  role TEXT, content TEXT, timestamp TEXT,
                  FOREIGN KEY (conversation_id) REFERENCES conversations(id))"""
    )
    conn.commit()
    conn.close()


def create_conversation():
    conn = sqlite3.connect("ariadne.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (created_at) VALUES (?)",
        (datetime.now().isoformat(),),
    )
    conversation_id = c.lastrowid
    conn.commit()
    conn.close()
    return conversation_id


def add_message(conversation_id, role, content):
    conn = sqlite3.connect("ariadne.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, role, content, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_conversation(conversation_id):
    conn = sqlite3.connect("ariadne.db")
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp",
        (conversation_id,),
    )
    messages = c.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in messages]

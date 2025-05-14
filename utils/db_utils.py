
import sqlite3
import pandas as pd
import os
import json
import hashlib
import numpy as np

def hash_task(grid: list[list], transformations: list[str]) -> str:
    np_grid = np.array(grid, dtype=np.uint8)
    grid_bytes = np_grid.tobytes()
    transformations_str = '|'.join(transformations)  # Use a delimiter unlikely to appear in your strings
    combined = grid_bytes + transformations_str.encode('utf-8')
    return hashlib.sha256(combined).hexdigest()

def access_db(db_name, db_path):
    """
    Create a connection to the database and return the cursor and connection object, 
    if the database does not exist, it will create it.
    """
    try:
        conn = sqlite3.connect(os.path.join(db_path, db_name.split('.db')[0] + ".db"))
    except Exception as e:
        raise Exception(f"Failed to connect to database: {e}")
    

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        i INTEGER PRIMARY KEY AUTOINCREMENT,
        task_key TEXT UNIQUE,
        task_hash TEXT UNIQUE,
        transformations TEXT
    )
    """)    
    conn.commit()
    return cursor, conn

def close_db(conn):
    conn.close()

def store_task_in_db(cursor, conn, task_key, task_hash, transformations, debug = False):
    try:
        cursor.execute("""
            INSERT INTO tasks (task_key, task_hash, transformations)
            VALUES (?, ?, ?)
        """, (task_key, task_hash, transformations))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        if debug:
            print(f"Duplicate detected: {task_hash} already exists. Skipping insertion.")
        return False  # Hash already exists

def load_tasks_to_dataframe(db_path):
    """Loads the entire tasks table from the database into a Pandas DataFrame."""
    conn = sqlite3.connect(os.path.join(db_path))
    query = "SELECT * FROM tasks"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
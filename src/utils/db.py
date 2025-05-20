import sqlite3
import os

def get_connection():
    this_file_path = os.path.abspath(__file__)
    utils_dir = os.path.dirname(this_file_path)
    src_dir = os.path.dirname(utils_dir)

    project_root = os.path.dirname(src_dir)

    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    db_file_path = os.path.join(data_dir, 'moonwind.db')
    conn = sqlite3.connect(db_file_path)

    return conn
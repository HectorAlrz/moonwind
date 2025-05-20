import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
QUERIES_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(QUERIES_DIR)

def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        print("Executing query: SELECT * FROM users;")
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        print(f"Fetched {len(users)} users from the database.")

        return users

if __name__ == '__main__':
    print("--- Running User Queries Script ---")

    retrieved_users = get_all_users()

    if retrieved_users:
        print("\n--- All Users ---")
        for user_row in retrieved_users:
            print("-" * 30)
            print(user_row)
    else:
        if not os.path.exists(os.path.join(SRC_DIR, 'data', 'moonwind.db')):
             print("Database file does not exist. Did you run database_setup.py and seed_data.py?")
        else:
            print("No users found in the database, or an error occurred.")
    print("--- End of User Queries Script ---")

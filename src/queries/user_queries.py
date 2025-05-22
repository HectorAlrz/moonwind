from enum import Enum
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
QUERIES_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(QUERIES_DIR)

class QueryMode(Enum):
    FETCH_ONE = 'fetch_one'
    FETCH_ALL = 'fetch_all'
    COMMIT = 'commit'
    NONE = 'none'

class UserQueries:
    def __init__(self):
        pass

    def _execute_query(self, query, params=None, mode = QueryMode.NONE):
        result = None
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")
                cursor.execute(query, params or ())
                result = None

                if mode == QueryMode.FETCH_ONE:
                    result = cursor.fetchone()
                    if result:
                        print(f"User with ID {params[0] if isinstance(params, tuple) and params else params} found: {result}")
                    else:
                        print(f"No user found with ID {params[0]}.")
                elif mode == QueryMode.FETCH_ALL:
                    result = cursor.fetchall()
                    print(f"Fetched {len(result)} users from the database.")
                elif mode == QueryMode.COMMIT:
                    conn.commit()
                    result = cursor.rowcount
                    print(f"Rows affected: {result}")

        except Exception as e:
            print(f"Database error in _execute_query: {e}")
        return result

    def get_all_users(self):
        return self._execute_query("SELECT * FROM users;", mode=QueryMode.FETCH_ALL)

    def get_user_by_id(self, user_id):
        return self._execute_query("SELECT * FROM users WHERE user_id = ?;", params=(user_id,), mode=QueryMode.FETCH_ONE)

    def create_user(self, username, email, password, full_name, settings):
        return self._execute_query(
            "INSERT INTO users (username, email, password, full_name, settings) VALUES (?, ?, ?, ?, ?);",
            params=(username, email, password, full_name, settings),
            mode=QueryMode.COMMIT
        )

    def update_user(self, user_id, username=None, email=None, password=None, full_name=None, settings=None, profile_picture=None):
        if not user_id:
            print("No user_id provided for update.")
            return 0

        update_fields = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name,
            "profile_picture": profile_picture
        }

        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        try:
            set_clause = ", ".join(f"{field} = ?" for field in update_fields)
            query = f"UPDATE users SET {set_clause} WHERE user_id = ?;"

            params = list(update_fields.values()) + [user_id]


            rows_affected = self._execute_query(query, params=tuple(params), mode=QueryMode.COMMIT)

            if rows_affected > 0:
                print(f"Successfully updated user with ID: {user_id}, affected rows: {rows_affected}, changes: {update_fields}")
            else:
                print(f"No changes made or user with ID: {user_id} not found")

            return rows_affected or 0

        except Exception as e:
            print(f"Error updating user with ID {user_id}: {str(e)}")
            raise


if __name__ == '__main__':
    print("--- Running User Queries Script ---")
    user_queries = UserQueries()
    #retrieved_users = user_queries.get_all_users()
    get_user = user_queries.get_user_by_id(1)
    #create_user = user_queries.create_user(username="Jotaro", email="fake@email.com", password="123", full_name="Jotaro Kujo", settings='{}')
    update_user = user_queries.update_user(1, username="Joe Dohn")

    # if retrieved_users:
    #     print("\n--- All Users ---")
    #     for user_row in retrieved_users:
    #         print("-" * 30)
    #         print(user_row)
    # else:
    #     if not os.path.exists(os.path.join(SRC_DIR, 'data', 'moonwind.db')):
    #          print("Database file does not exist. Did you run database_setup.py and seed_data.py?")
    #     else:
    #         print("No users found in the database, or an error occurred.")
    print("--- End of User Queries Script ---")

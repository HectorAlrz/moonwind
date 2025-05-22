import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection


def get_all_users():
    query = "SELECT * FROM users;"
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Fetched {len(result)} users from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_all_users: {e}")
        return None

# 1.- Listar todas las historias (story) junto con el nombre completo del usuario que las creó
# y su estado (si está destacada o es pública).
def get_all_stories():
    query = "SELECT title, is_starred, is_public, full_name AS created_by FROM story JOIN users ON users.user_id = story.created_by;"
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_all_stories: {e}")
        return None

# 2.- Obtener todas las listas (lists) y sus respectivas tarjetas (cards) para una historia específica,
# mostrando el título de la lista y los títulos de cada tarjeta en orden de posición.
def get_lists_and_cards_by_story_id(story_id):
    query = """
    SELECT story.title as story_title,
          lists.title as list_title,
          cards.title as card_title
    FROM story
    JOIN lists ON lists.story_id = story.story_id
    JOIN cards ON cards.list_id = lists.list_id
    WHERE story.story_id = ?
    ORDER BY lists.position, cards.position;
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query, (story_id,))
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_lists_and_cards_by_story_id: {e}")
        return None


## Consultar los comentarios realizados en una tarjeta específica, incluyendo el nombre del usuario que hizo
# el comentario y el contenido del mismo, ordenados por fecha de creación.
def get_comments_by_card_id(card_id):
    query ="""
    SELECT users.username, comments.content, comments.card_id, comments.created_at FROM comments
    JOIN users ON comments.user_id = users.user_id
    WHERE comments.card_id = ?
    ORDER BY comments.created_at
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query, (card_id,))
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_comments_by_card_id: {e}")
        return None

# Generar un reporte de todos los usuarios asignados a cada tarjeta, mostrando el título de la tarjeta,
# el nombre completo del usuario y la fecha de asignación.
def get_cards_assigned_users():
    query ="""
      SELECT cards.title AS card_title, users.full_name, assigned_at FROM card_assigned_users
      JOIN cards ON card_assigned_users.card_id = cards.card_id
      JOIN users ON users.user_id = card_assigned_users.user_id
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_all_users: {e}")
        return None

# Obtener un listado de todos los miembros (story_members) de una historia específica,
# incluyendo su rol (admin o miembro) y la fecha en que se unieron
def get_story_members(story_id):
    query ="""
      SELECT story.title AS story_title, users.full_name, story_members.role, story_members.joined_at FROM story_members
      JOIN users ON users.user_id = story_members.user_id
      JOIN story ON story.story_id = story_members.story_id
      WHERE story_members.story_id = ?
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query, (story_id,))
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_all_users: {e}")
        return None

# Calcular cuántas historias ha creado cada usuario y cuántas
# de estas están marcadas como destacadas (is_starred = 1).
def get_stories_per_user():
    query ="""
      SELECT
      users.full_name, story.created_by,
      COUNT(story.story_id) AS total_stories,
      COUNT(CASE WHEN is_starred = 1 THEN 1 END)
      FROM story
      JOIN users ON users.user_id = story.created_by
      GROUP BY users.user_id
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Fetched {len(result)} results from the database.")
            return result
    except Exception as e:
        print(f"Database error in get_all_users: {e}")
        return None


if __name__ == '__main__':
  print("--- Running User Queries Script ---")
  #  users = get_all_users()
  # stories = get_all_stories()
  # get_all_story = get_lists_and_cards_by_story_id(1)
  # get_comments_by_card_id = get_comments_by_card_id(1)
  # get_cards_assigned_users = get_cards_assigned_users()
  # get_story_members = get_story_members(1)
  get_stories_per_user = get_stories_per_user()

# WARNING: Cambiar el nombre de la variable dependiendo de la consulta :)
  for row in get_stories_per_user:
    print(dict(row))

  print("--- End of User Queries Script ---")

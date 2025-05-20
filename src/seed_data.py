import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DB_FILENAME = 'moonwind.db'

DB_PATH = os.path.join(PROJECT_ROOT_DIR, 'data', DB_FILENAME)

def insert_data():
    data_dir = os.path.join(PROJECT_ROOT_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print(f"Data already seems to exist in '{DB_NAME}'. Skipping insertion to avoid duplicates.")
        conn.close()
        return

    users_data = [
        ('john_doe', 'john@example.com', 'pass1', 'John Doe', '{"theme": "dark", "notifications": {"email": true, "push": false}}'),
        ('jane_smith', 'jane@example.com', 'pass2', 'Jane Smith', '{"theme": "light", "notifications": {"email": false, "push": true}}'),
        ('bob_johnson', 'bob@example.com', 'pass3', 'Bob Johnson', '{"theme": "auto", "notifications": {"email": true, "push": true}}'),
        ('alice_williams', 'alice@example.com', 'pass', 'Alice Williams', '{"theme": "dark", "notifications": {"email": false, "push": false}}'),
        ('charlie_brown', 'charlie@example.com', 'pass5', 'Charlie Brown', '{"theme": "light", "notifications": {"email": true, "push": true}}')
    ]
    cursor.executemany("INSERT INTO users (username, email, password, full_name, settings) VALUES (?, ?, ?, ?, ?)", users_data)

    story_data = [
        ('Work Projects', 'All company projects', 1, 0, 1), ('Personal Tasks', 'My personal to-do list', 1, 0, 1),
        ('Travel Plans', 'Upcoming trips and ideas', 0, 1, 2), ('Team Roadmap', 'Product development roadmap', 1, 0, 3),
        ('Study Materials', 'Course notes and resources', 0, 1, 4)
    ]
    cursor.executemany("INSERT INTO story (title, description, is_starred, is_public, created_by) VALUES (?, ?, ?, ?, ?)", story_data)

    lists_data = [
        (1, 'To Do', 1), (1, 'In Progress', 2), (1, 'Testing', 3), (1, 'Done', 4), (2, 'Backlog', 1),
        (2, 'This Week', 2), (2, 'Today', 3), (2, 'Completed', 4), (3, 'Ideas', 1), (3, 'Planning', 2),
        (3, 'Booked', 3), (4, 'Q1 Goals', 1), (4, 'Q2 Goals', 2), (4, 'Q3 Goals', 3), (4, 'Q4 Goals', 4),
        (5, 'Resources', 1), (5, 'Notes', 2), (5, 'Assignments', 3)
    ]
    cursor.executemany("INSERT INTO lists (story_id, title, position) VALUES (?, ?, ?)", lists_data)

    cards_data = [
        (1, 'Design new landing page', 'Create wireframes for homepage redesign', 1, '2025-05-01 12:00:00', 1),
        (1, 'Fix login bug', 'Users reported issues with social login', 2, '2025-04-22 15:00:00', 1),
        (2, 'Implement user authentication', 'Add OAuth integration', 1, '2025-04-25 17:00:00', 3),
        (3, 'Test payment gateway', 'Verify all payment flows', 1, '2025-04-20 12:00:00', 2),
        (4, 'Database optimization', 'Improved query performance', 1, None, 3),
        (5, 'Learn advanced SQL', 'Study advanced SQL techniques', 1, '2025-05-10 09:00:00', 1),
        (6, 'Grocery shopping', 'Get items for dinner party', 1, '2025-04-19 18:00:00', 1),
        (7, 'Call dentist', 'Schedule annual checkup', 1, '2025-04-19 10:00:00', 1),
        (8, 'File taxes', 'Completed annual tax filing', 1, None, 1),
        (9, 'Visit Japan', 'Tokyo, Kyoto, and Osaka trip ideas', 1, None, 2),
        (10, 'Summer road trip', 'Plan route, accommodations', 1, '2025-06-15 12:00:00', 2),
        (11, 'Weekend getaway', 'Cabin reservation confirmed', 1, '2025-05-05 15:00:00', 2),
        (12, 'Improve website performance', 'Optimize loading speed', 1, '2025-03-30 12:00:00', 3),
        (13, 'Launch mobile app', 'Release MVP version', 1, '2025-06-15 12:00:00', 3),
        (14, 'Expand to European market', 'Research regulations', 1, '2025-09-01 12:00:00', 3),
        (15, 'Annual review', 'Prepare reports for stakeholders', 1, '2025-12-15 12:00:00', 3),
        (16, 'Programming books', 'Collection of resources', 1, None, 4),
        (17, 'Chapter 5 summary', 'Key concepts from databases', 1, '2025-04-25 23:59:00', 4),
        (18, 'Final project proposal', 'Submit project idea', 1, '2025-05-01 23:59:00', 4)
    ]
    cursor.executemany("INSERT INTO cards (list_id, title, description, position, due_date, created_by) VALUES (?, ?, ?, ?, ?, ?)", cards_data)

    comments_data = [
        (1, 2, 'I suggest using the new brand colors for this design.'), (1, 1, "Good idea! I'll update the wireframes."),
        (2, 3, 'I think the issue is with the token expiration.'), (4, 2, 'All tests passed on my end.'),
        (4, 3, "Great! Let's move this to production then."), (9, 2, 'I found a great deal on flights for May!'),
        (9, 4, 'I recommend visiting during cherry blossom season.'), (12, 3, 'We should prioritize image optimization.'),
        (12, 5, 'I can help with the CDN setup.'), (17, 4, "Don't forget to include the normalization section."),
        (18, 4, 'How many pages should this proposal be?')
    ]
    cursor.executemany("INSERT INTO comments (card_id, user_id, content) VALUES (?, ?, ?)", comments_data)

    story_members_data = [
        (1, 1, 'admin'), (2, 1, 'member'), (3, 1, 'member'), (5, 1, 'member'), (1, 2, 'admin'),
        (2, 3, 'admin'), (1, 3, 'member'), (4, 3, 'member'), (3, 4, 'admin'), (1, 4, 'member'),
        (2, 4, 'member'), (5, 4, 'member'), (4, 5, 'admin'), (5, 5, 'member')
    ]
    cursor.executemany("INSERT INTO story_members (user_id, story_id, role) VALUES (?, ?, ?)", story_members_data)

    card_assigned_users_data = [
        (1, 1), (2, 1), (1, 2), (3, 2), (3, 3), (5, 3), (2, 4), (3, 4), (3, 5), (1, 6), (1, 7),
        (1, 8), (2, 9), (4, 9), (2, 10), (1, 10), (2, 11), (3, 12), (5, 12), (3, 13), (1, 13),
        (2, 13), (3, 14), (2, 14), (3, 15), (1, 15), (4, 16), (5, 16), (4, 17), (4, 18)
    ]
    cursor.executemany("INSERT INTO card_assigned_users (user_id, card_id) VALUES (?, ?)", card_assigned_users_data)

    conn.commit()
    conn.close()
    print("-" * 30)
    print(f"Data inserted successfully into '{DB_PATH}'.")
    print("-" * 30)

if __name__ == '__main__':
    insert_data()

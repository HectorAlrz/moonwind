-- db para app tipo shortcut --

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT,
    profile_picture TEXT,
    settings TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE story (
    story_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    is_starred BOOLEAN DEFAULT 0,
    is_public BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE lists (
    list_id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    position REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived BOOLEAN DEFAULT 0,
    FOREIGN KEY (story_id) REFERENCES story(story_id)
);

CREATE TABLE cards (
    card_id INTEGER PRIMARY KEY,
    list_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    position REAL NOT NULL,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    archived BOOLEAN DEFAULT 0,
    FOREIGN KEY (list_id) REFERENCES lists(list_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    card_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (card_id) REFERENCES cards(card_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE story_members (
    user_id INTEGER NOT NULL,
    story_id INTEGER NOT NULL,
    role TEXT DEFAULT 'member' CHECK(role IN ('admin', 'member')),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, story_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (story_id) REFERENCES story(story_id)
);

CREATE TABLE card_assigned_users (
    user_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, card_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);

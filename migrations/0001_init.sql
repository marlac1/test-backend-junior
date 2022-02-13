CREATE TABLE players (
    id VARCHAR PRIMARY KEY,
    nickname VARCHAR UNIQUE NOT NULL,
    phone_number VARCHAR UNIQUE NOT NULL,
    gender VARCHAR
);
create table conversations (
    id VARCHAR PRIMARY KEY,
    archived BOOLEAN DEFAULT FALSE,
    created_at DATETIME not null
);
create table conversation_messages (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR NOT NULL REFERENCES conversations (id) ON UPDATE CASCADE ON DELETE CASCADE,
    send_by VARCHAR NOT NULL REFERENCES players (id) ON UPDATE CASCADE ON DELETE CASCADE,
    content VARCHAR,
    attachments JSON,
    metadata JSON,
    send_at DATETIME not null,
    UNIQUE (id, conversation_id, send_by)
);
create table conversation_players (
    conversation_id VARCHAR NOT NULL REFERENCES conversations (id) ON UPDATE CASCADE ON DELETE CASCADE,
    player_id VARCHAR NOT NULL REFERENCES players (id) ON UPDATE CASCADE ON DELETE CASCADE,
    last_read VARCHAR REFERENCES messages (id) ON UPDATE CASCADE ON DELETE SET NULL,
    last_sent VARCHAR REFERENCES messages (id) ON UPDATE CASCADE ON DELETE SET NULL,
    masked BOOLEAN NOT NULL DEFAULT FALSE
);
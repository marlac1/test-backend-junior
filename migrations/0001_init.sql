CREATE TABLE players (
    id VARCHAR PRIMARY KEY,
    nickname VARCHAR UNIQUE NOT NULL,
    phone_number VARCHAR UNIQUE NOT NULL,
    gender VARCHAR
);
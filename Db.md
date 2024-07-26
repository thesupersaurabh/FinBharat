sqlite3 finbharat.db

-- Create 'users' table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000000.00
);

-- Create 'transactions' table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    symbol TEXT,
    shares INTEGER,
    price REAL,
    date DATETIME
);

-- Create unique index on 'username' in 'users' table
CREATE UNIQUE INDEX username ON users (username);

.exit
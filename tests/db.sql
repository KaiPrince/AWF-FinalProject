DROP TABLE IF EXISTS account;
CREATE TABLE account (
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
hash BLOB NOT NULL,
salt BLOB NOT NULL
);

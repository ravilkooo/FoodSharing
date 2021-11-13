CREATE TABLE IF NOT EXISTS guestmenu(
id integer PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    surname text NOT NULL,
    phone text NOT NULL,
    email text NOT NULL,
    psw text NOT NULL,
    avatar BLOB DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS users_roles(
    user_id integer PRIMARY KEY,
    role integer NOT NULL
);


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
    avatar BLOB DEFAULT NULL,
    banned INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS users_roles(
    user_id integer PRIMARY KEY,
    role_id integer NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS roles(
    id integer PRIMARY KEY NOT NULL,
    role text NOT NULL
);
CREATE TABLE IF NOT EXISTS groups(
    vol_id integer NOT NULL,
    coord_id integer NOT NULL,
    group_id integer NOT NULL,
    area text NOT NULL
);
CREATE TABLE IF NOT EXISTS partners(
    partner_id integer NOT NULL PRIMARY KEY,
    name text NOT NULL,
    phone text NOT NULL,
    address text NOT NULL
);
CREATE TABLE IF NOT EXISTS groups_partners(
    group_id integer PRIMARY KEY NOT NULL,
    partner_id integer NOT NULL
);
CREATE TABLE IF NOT EXISTS acts(
    id integer PRIMARY KEY NOT NULL,
    group_id integer NOT NULL,
    partner_id integer NOT NULL,
    date integer NOT NULL,
    status integer NOT NULL
);
CREATE TABLE IF NOT EXISTS products(
    name text NOT NULL,
    amount integer NOT NULL,
    price_per float NOT NULL,
    shelf_life integer NOT NULL,
    act_id integer NOT NULL,
    user_id integer NOT NULL
);

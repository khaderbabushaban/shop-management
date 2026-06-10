CREATE TABLE Sections (
    section_id SERIAL PRIMARY KEY,
    section_name VARCHAR(100) NOT NULL
);

CREATE TABLE Sellers (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    section_id INTEGER REFERENCES Sections(section_id),
    salary NUMERIC NOT NULL
);

CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE Items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    section_id INTEGER REFERENCES Sections(section_id)
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES Customers(customer_id),
    item_id INTEGER REFERENCES Items(item_id),
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;
INSERT INTO users (username, password, user_type) VALUES ('khader', crypt('khader123', gen_salt('bf')), 'admin');
INSERT INTO users (username, password, user_type) VALUES ('ahmed', crypt('ahmed123', gen_salt('bf')), 'seller');
INSERT INTO users (username, password, user_type) VALUES ('noor', crypt('noor125', gen_salt('bf')), 'seller');
INSERT INTO users (username, password, user_type) VALUES ('mohamed', crypt('moha125', gen_salt('bf')), 'seller');
INSERT INTO users (username, password, user_type) VALUES ('ayman', crypt('2563658', gen_salt('bf')), 'seller');
INSERT INTO users (username, password, user_type) VALUES ('jack', crypt('jack52369', gen_salt('bf')), 'seller');
INSERT INTO users (username, password, user_type) VALUES ('karam', crypt('karam5236', gen_salt('bf')), 'seller');

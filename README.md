# tienda
DROP DATABASE IF EXISTS tienda;
CREATE DATABASE tienda CHARSET utf8mb4;
USE tienda;

CREATE TABLE tienda (
    id SERIAL PRIMARY KEY,
    nombre_tienda TEXT NOT NULL
);

CREATE TABLE objetos_en_tienda (
    id SERIAL PRIMARY KEY,
    nombre_tienda TEXT NOT NULL,
    nombre_objeto TEXT NOT NULL,
    precio INTEGER,
    stock INTEGER
);
INSERT INTO tienda (nombre_tienda) VALUES
  ('Tienda Pikachu'),
  ('Tienda Charmander'),
  ('Tienda Squirtle');


INSERT INTO objetos_en_tienda (nombre_tienda, nombre_objeto, precio, stock) VALUES
  ('Tienda Pikachu', 'Pokebola', 100, 50),
  ('Tienda Charmander', 'Piedra Fuego', 150, 30),
  ('Tienda Squirtle', 'Poción', 200, 20);

CREATE DATABASE IF NOT EXISTS CentroAdopcion;
USE CentroAdopcion;

-- Basado en la clase Person
CREATE TABLE IF NOT EXISTS Person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    lastName VARCHAR(100),
    age INT,
    dateOfBirth DATE,
    id_card VARCHAR(20) UNIQUE, -- El 'ID: string' de tu diagrama
    cel INT,
    email VARCHAR(100)
);

-- Basado en la clase Adopter, hereda de Person
CREATE TABLE IF NOT EXISTS Adopter (
    person_id INT PRIMARY KEY,
    address VARCHAR(200),
    FOREIGN KEY (person_id) REFERENCES Person(id)
);

-- Basado en las clases Pet y Dog
CREATE TABLE IF NOT EXISTS Dog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    adopted BOOLEAN DEFAULT FALSE,
    breed VARCHAR(50) -- Detalle específico de perro
);

-- Insertamos los 3 perros en catálogo
INSERT INTO Dog (name, age, breed) VALUES 
('Firulais', 3, 'Labrador'),
('Rex', 5, 'Pastor Alemán'),
('Luna', 2, 'Husky');
-- 🚫 1. Borrar base de datos anterior si existe
DROP DATABASE IF EXISTS prototipo;

-- 🆕 2. Crear base de datos nueva
CREATE DATABASE prototipo;
USE prototipo;

-- 🏢 3. Crear tabla TERMINAL
CREATE TABLE TERMINAL (
    numero INT PRIMARY KEY,
    terNumero VARCHAR(10),
    terCalle VARCHAR(50),
    terColonia VARCHAR(50)
);

-- Insertar una terminal de ejemplo
INSERT INTO TERMINAL (numero, terNumero, terCalle, terColonia)
VALUES (1, 'T001', 'Av. Reforma', 'Centro');

-- 👨‍💼 4. Crear tabla TAQUILLERO con AUTO_INCREMENT
CREATE TABLE TAQUILLERO (
    registro INT AUTO_INCREMENT PRIMARY KEY,
    taqNombre VARCHAR(50),
    taqPrimerApell VARCHAR(50),
    taqSegundoApell VARCHAR(50),
    fechaContrato DATE,
    usuario VARCHAR(30) UNIQUE,
    contraseña VARCHAR(100),
    terminal INT,
    FOREIGN KEY (terminal) REFERENCES TERMINAL(numero)
);

-- ✅ Confirmación de estructura
SHOW TABLES;
DESCRIBE TAQUILLERO;

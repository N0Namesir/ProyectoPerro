"""
setup_db.py — Inicializa la base de datos con las tablas y datos de prueba.
Ejecutar UNA sola vez antes de arrancar la app:

    python setup_db.py

Si las tablas ya existen, no las sobreescribe (IF NOT EXISTS).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

import config

SQL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS Person (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        name       VARCHAR(100),
        lastName   VARCHAR(100),
        age        INT,
        dateOfBirth DATE,
        id_card    VARCHAR(20) UNIQUE,
        cel        BIGINT,
        email      VARCHAR(100)
    )
    """,
    # FIX: se agregó dog_id (con FK a Dog) que faltaba en la definición original
    """
    CREATE TABLE IF NOT EXISTS Dog (
        id      INT AUTO_INCREMENT PRIMARY KEY,
        name    VARCHAR(50),
        age     INT,
        adopted BOOLEAN DEFAULT FALSE,
        breed   VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Adopter (
        person_id INT PRIMARY KEY,
        address   VARCHAR(200),
        dog_id    INT NOT NULL,
        FOREIGN KEY (person_id) REFERENCES Person(id),
        FOREIGN KEY (dog_id) REFERENCES Dog(id)
    )
    """,
    # Solo inserta los perros si la tabla estaba vacía
    """
    INSERT IGNORE INTO Dog (id, name, age, breed) VALUES
        (1, 'Firulais', 3, 'Labrador'),
        (2, 'Rex',      5, 'Pastor Alemán'),
        (3, 'Luna',     2, 'Husky')
    """
]

def run():
    conn = config.get_db_connection()
    if not conn:
        print("[ERROR] No se pudo conectar. Revisa tu configuración en app/config.py")
        sys.exit(1)

    cur = conn.cursor()
    for sql in SQL_STATEMENTS:
        try:
            cur.execute(sql)
        except Exception as e:
            print(f"[WARN] {e}")

    conn.commit()
    conn.close()
    print("[OK] Base de datos inicializada correctamente.")

if __name__ == '__main__':
    run()
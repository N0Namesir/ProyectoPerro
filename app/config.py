import mariadb

# Configuración de conexión. Cámbialo por tus credenciales.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "tu_usuario_mariadb",
    "password": "tu_contraseña_mariadb",
    "database": "CentroAdopcion"
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return None
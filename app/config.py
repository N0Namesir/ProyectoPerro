import os
import mariadb

# Lee desde variables de entorno; si no existen, usa valores locales por defecto.
# En Docker, las variables se inyectan desde docker-compose.yml.
# En local, se usan los valores de fallback (modifícalos según tu instalación).
DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "localhost"),
    "port":     int(os.environ.get("DB_PORT", 3306)),
    "user":     os.environ.get("DB_USER", "user_perro"),
    "password": os.environ.get("DB_PASS", "password123"),
    "database": os.environ.get("DB_NAME", "proyectoperro")
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"[ERROR] No se pudo conectar a MariaDB: {e}")
        print(f"[INFO]  Configuración usada: host={DB_CONFIG['host']} "
              f"user={DB_CONFIG['user']} db={DB_CONFIG['database']}")
        return None
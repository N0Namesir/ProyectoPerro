import config

def get_available_dogs():
    conn = config.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, breed FROM Dog WHERE adopted = FALSE")
    dogs_data = cur.fetchall()
    conn.close()
    return dogs_data

def get_dog_by_id(dog_id):
    conn = config.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, breed FROM Dog WHERE id = ?", (dog_id,))
    dog_data = cur.fetchone()
    conn.close()
    return dog_data

def register_adoption_transactional(dog_id, adopter_name, adopter_lastname, address, id_card):
    conn = config.get_db_connection()
    if not conn: return False
    
    cur = conn.cursor()
    try:
        # Iniciar una transacción para asegurar integridad
        conn.autocommit = False
        
        # 1. Registrar a la Persona
        sql_person = "INSERT INTO Person (name, lastName, id_card) VALUES (?, ?, ?)"
        cur.execute(sql_person, (adopter_name, adopter_lastname, id_card))
        person_id = cur.lastrowid
        
        # 2. Registrar al Adoptante (herencia de Person)
        sql_adopter = "INSERT INTO Adopter (person_id, address) VALUES (?, ?)"
        cur.execute(sql_adopter, (person_id, address))
        
        # 3. Actualizar el estado del perro
        sql_dog = "UPDATE Dog SET adopted = TRUE WHERE id = ?"
        cur.execute(sql_dog, (dog_id,))
        
        # Guardar todos los cambios
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error en la transacción de adopción: {e}")
        # Revertir todo si algo sale mal
        conn.rollback()
        return False
    finally:
        conn.close()
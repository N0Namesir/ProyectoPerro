from flask import Flask, render_template, request, redirect, url_for
import database
import models

app = Flask(__name__)

@app.route('/')
def index():
    # Recuperamos los perros del catálogo real
    dogs_data = database.get_available_dogs()
    # Podemos convertir los datos a objetos 'Dog' si quisiéramos usar métodos de la clase
    available_dogs = [models.Dog(row[0], row[1], row[2], row[3]) for row in dogs_data]
    
    return render_template('catalogo.html', dogs=available_dogs)

@app.route('/adoptar/<int:dog_id>')
def form_adopcion(dog_id):
    dog = database.get_dog_by_id(dog_id)
    if not dog:
        return "Perrito no encontrado", 404
    dog_obj = models.Dog(dog[0], dog[1], dog[2], dog[3])
    return render_template('confirmacion.html', dog=dog_obj)

@app.route('/confirmar_adopcion', methods=['POST'])
def procesar_adopcion():
    # Recibimos datos del formulario de la web
    dog_id = request.form['dog_id']
    name = request.form['name']
    lastname = request.form['lastname']
    address = request.form['address']
    id_card = request.form['id_card']
    
    # Ejecutamos la lógica de negocio modular
    success = database.register_adoption_transactional(dog_id, name, lastname, address, id_card)
    
    if success:
        dog = database.get_dog_by_id(dog_id)
        return f"<h1>¡Felicidades! Has adoptado a {dog[1]} exitosamente.</h1><a href='/'>Volver al catálogo</a>"
    else:
        return "Error al procesar la adopción. Por favor, inténtalo de nuevo."

if __name__ == '__main__':
    # Asegúrate de que las tablas estén creadas antes de correr la web.
    app.run(debug=True, host='0.0.0.0', port=5000)
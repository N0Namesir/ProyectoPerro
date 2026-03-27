import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from flask import Flask, render_template, request, redirect, url_for
import database
import models

app = Flask(__name__, template_folder='../templates')

# ─── RUTAS PÚBLICAS ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    dogs_data = database.get_available_dogs()
    available_dogs = [models.Dog(r[0], r[1], r[2], r[3]) for r in dogs_data]
    return render_template('catalogo.html', dogs=available_dogs)


@app.route('/adoptar/<int:dog_id>')
def form_adopcion(dog_id):
    dog_data = database.get_dog_by_id(dog_id)
    if not dog_data:
        return render_template('error.html', mensaje="Perrito no encontrado."), 404
    if dog_data[4]:  # adopted == True
        return render_template('error.html', mensaje="Este perrito ya fue adoptado. ¡Qué buena noticia!"), 400
    dog = models.Dog(dog_data[0], dog_data[1], dog_data[2], dog_data[3])
    return render_template('confirmacion.html', dog=dog)


@app.route('/confirmar_adopcion', methods=['POST'])
def procesar_adopcion():
    dog_id   = request.form['dog_id']
    name     = request.form['name'].strip()
    lastname = request.form['lastname'].strip()
    address  = request.form['address'].strip()
    id_card  = request.form['id_card'].strip()

    # Validación básica
    if not all([name, lastname, address, id_card]):
        return render_template('error.html', mensaje="Todos los campos son obligatorios."), 400

    success = database.register_adoption_transactional(dog_id, name, lastname, address, id_card)

    if success:
        dog_data = database.get_dog_by_id(dog_id)
        dog = models.Dog(dog_data[0], dog_data[1], dog_data[2], dog_data[3])
        return render_template('exito.html', dog=dog, adopter_name=name)
    else:
        return render_template('error.html',
            mensaje="Error al procesar la adopción. Es posible que la cédula ya esté registrada."), 500


# ─── RUTAS DE ADMINISTRACIÓN ─────────────────────────────────────────────────

@app.route('/admin')
def admin():
    all_dogs    = database.get_all_dogs()
    adoptions   = database.get_all_adoptions()
    dogs_objs   = [models.Dog(r[0], r[1], r[2], r[3], r[4]) for r in all_dogs]
    return render_template('admin.html', dogs=dogs_objs, adoptions=adoptions)


@app.route('/admin/agregar_perro', methods=['POST'])
def agregar_perro():
    name  = request.form['name'].strip()
    age   = request.form['age'].strip()
    breed = request.form['breed'].strip()

    if not all([name, age, breed]):
        return render_template('error.html', mensaje="Todos los campos del perro son obligatorios."), 400

    success = database.add_dog(name, age, breed)
    if success:
        return redirect(url_for('admin'))
    else:
        return render_template('error.html', mensaje="No se pudo agregar el perro."), 500


@app.route('/admin/eliminar/<int:dog_id>', methods=['POST'])
def eliminar_perro(dog_id):
    success = database.delete_dog(dog_id)
    if success:
        return redirect(url_for('admin'))
    else:
        return render_template('error.html',
            mensaje="No se puede eliminar: el perro no existe o ya fue adoptado."), 400
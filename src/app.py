"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    # Validamos si existe el array de la familia
    if members:
        return jsonify(members), 200
    else:
        return jsonify("No encontrado"), 400

@app.route('/member/<int:id>', methods=['GET'])
def members(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)

    # Validamos si existe el miembro de la familia
    if member:
        return jsonify(member), 200
    else:
        return jsonify("No encontrado"), 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete(id):

    # this is how you can use the Family datastructure by calling its methods
    # Intentamos eliminar al miembro
    success = jackson_family.delete_member(id)
    if not success:  # Si no se pudo eliminar, devolvemos un error 404
        response_body = {
            "done": False,
        }
        return jsonify(response_body), 404  # Código de error 404 (no encontrado)
    
    # Si la eliminación fue exitosa, devolvemos una respuesta positiva
    response_body = {
        "done": True,
    }
    return jsonify(response_body), 200  # Código 200 (OK)
    
    
@app.route('/member', methods=['POST'])
def add():

    # this is how you can use the Family datastructure by calling its methods
    body = request.get_json()

    # Verificar que los datos recibidos tienen la estructura esperada
    if not body or not isinstance(body, dict):
        return jsonify({"error": "Invalid data format"}), 400

    # Validación de campos necesarios
    required_fields = ["first_name", "age", "lucky_numbers"]

    # Verificar que todos los campos requeridos están presentes
    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"No se encuentra el campo: {field}"}), 400
        
    # Validar "age" (debe ser un número entero positivo)
    if not isinstance(body["age"], int) or body["age"] <= 0:
        return jsonify("age debe ser unun numero entero"), 400
    
    # Validar "lucky_numbers" (debe ser una lista de enteros)
    if not isinstance(body["lucky_numbers"], list) or not all(isinstance(num, int) for num in body["lucky_numbers"]):
        return jsonify("lucky_numbers debe ser una lista de enteros."), 400

    # Validar "first_name" (debe ser una cadena no vacía)
    if not isinstance(body["first_name"], str) or not body["first_name"]:
        return jsonify("first_name debe tener contenido."), 400
    
    else:
        # Llamar al método add_member para agregar el miembro
        member = jackson_family.add_member(body)
        
        # Retornar la respuesta con el miembro agregado
        return jsonify(member), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

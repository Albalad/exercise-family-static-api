# Add the jsonify method to your Flask import
from flask import Flask, jsonify, request
app = Flask(__name__)
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = [
            {
                "id": 1,
                "first_name": "John",
                "last_name":  "Jackson",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": 2,
                "first_name": "Jane",
                "last_name":  "Jackson",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": 3,
                "first_name": "Jimmy",
                "last_name":  "Jackson",
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)
 
    def add_member(self, member):
        # Verificar si el miembro tiene un 'id', si no lo tiene, se genera uno
        if "id" not in member or not member["id"]:
            member['id'] = self._generateId()  # Generar un nuevo ID

        # Verificar si el miembro tiene un 'last_name', si no lo tiene, usar el 'last_name' global
        if "last_name" not in member:
            member['last_name'] = self.last_name

        # Agregar el miembro a la lista de miembros
        self._members.append(member)
        
        # Retornar el miembro agregado con el ID asignado
        return member

    def delete_member(self, id):
        # Busca y elimina el miembro con el id proporcionado
        for member in self._members:
            if member['id'] == id:
                self._members.remove(member)
                return True  # Miembro eliminado con éxito
        return False  # No se encontró el miembro con ese id
     
    def get_member(self, id):
        # fill this method and update the return 
        for member in self._members:
            if member['id'] == id:
                return member

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members


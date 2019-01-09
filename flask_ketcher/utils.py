from functools import wraps

from flask import request, jsonify
from indigo import Indigo, IndigoException


def with_indigo_option(func):
    @wraps(func)
    def wrapper():
        indigo = Indigo()
        opts = request.json.get('options', {})
        for key, value in opts.items():
            indigo.setOption(key, value)
        return func()
    return wrapper


def load_molecule_from_request(func):
    @wraps(func)
    def wrapper():
        indigo = Indigo()
        opts = request.json.get('options', {})
        for key, value in opts.items():
            try:
                indigo.setOption(key, value)
            except IndigoException as e:
                pass
        mol_text = request.json.get("struct")
        try:
            mol = indigo.loadMolecule(mol_text)
        except IndigoException as e:
            return jsonify({'msg': str(e)})
        return func(mol)
    return wrapper

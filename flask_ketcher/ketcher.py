from uuid import uuid4

from flask import Blueprint, request, jsonify
from indigo import Indigo
from flask import current_app as app
from os import path

try:
    from pyimago import imago
except ModuleNotFoundError:
    imago = None

from flask_ketcher.utils import load_molecule_from_request

indigo = Indigo()
ketcher = Blueprint('ketcher', __name__, url_prefix='/ketcher', static_folder='static', static_url_path='/')


@ketcher.route('/ketcher.html')
def editor():
    return ketcher.send_static_file("ketcher.html")


# For debug use
@ketcher.route('/demo.html')
def demo():
    return ketcher.send_static_file("demo.html")


# TODO
@ketcher.route('/info')
def info():
    d = {
        "indigo_version": indigo.version(),
        "imago_versions": [imago and imago.version(), ],
    }
    return jsonify(d)


# TODO Not sure what it suppose to be
@ketcher.route('/indigo/calculate_cip', methods=['POST', ])
@load_molecule_from_request
def calculate_cip(mol=None):
    mol.markEitherCisTrans()
    mol.markStereobonds()
    d = {'struct': mol.molfile()}
    return jsonify(d)


@ketcher.route('/indigo/calculate', methods=['POST', ])
@load_molecule_from_request
def calculate(mol=None):
    d = {
        'molecular-weight': mol.molecularWeight(),
        'most-abundant-mass': mol.mostAbundantMass(),
        'monoisotopic-mass': mol.monoisotopicMass(),
        'gross': mol.grossFormula(),
        'mass-composition': mol.massComposition(),
    }
    return jsonify(d)


# TODO Unknown types usage
@ketcher.route('/indigo/check', methods=['POST', ])
@load_molecule_from_request
def check(mol=None):
    # types = request.json.get('types')
    ts = ('checkBadValence', 'checkAmbiguousH')
    errs = []
    for t in ts:
        func = getattr(mol, t)
        if func is None:
            continue
        err = func()
        if err:
            errs.append(err)
    return jsonify(errs)


@ketcher.route('/indigo/aromatize', methods=['POST', ])
@load_molecule_from_request
def aromatize(mol=None):
    mol.aromatize()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@ketcher.route('/indigo/dearomatize', methods=['POST', ])
@load_molecule_from_request
def dearomatize(mol=None):
    mol.dearomatize()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@ketcher.route('/indigo/layout', methods=['POST', ])
@load_molecule_from_request
def layout(mol=None):
    mol.layout()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@ketcher.route('/indigo/clean', methods=['POST', ])
@load_molecule_from_request
def clean(mol=None):
    mol.clean2d()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


# TODO
@ketcher.route('/imago/uploads', methods=['POST', ])
def uploads():
    fname = f"{uuid4()}"
    fp = path.join(app.root_path, app.config['UPLOAD_FOLDER'], fname)
    with open(fp, 'wb') as f:
        f.write(request.data)
    d = {
        'upload_id': fname,
    }
    return jsonify(d)


# TODO
@ketcher.route('/imago/uploads/<file_id>', methods=['GET', ])
def recognize(file_id):
    fp = path.join(app.root_path, app.config['UPLOAD_FOLDER'], file_id)
    mol = imago.get_mol_text_from_fp(fp)
    d = {
        "state": "SUCCESS",
        "metadata": {"mol_str": mol},
    }
    return jsonify(d)

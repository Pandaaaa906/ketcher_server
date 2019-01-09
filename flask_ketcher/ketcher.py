from uuid import uuid4

from flask import Blueprint, request, jsonify
from indigo import Indigo
from flask import current_app as app
from os import path

from flask_ketcher.utils import load_molecule_from_request

indigo = Indigo()
bp = Blueprint('ketcher', __name__, url_prefix='/ketcher', static_folder='static', static_url_path='/')


@bp.route('/ketcher.html')
def ketcher():
    return bp.send_static_file("ketcher.html")


# For debug use
@bp.route('/demo.html')
def demo():
    return bp.send_static_file("demo.html")


# TODO
@bp.route('/info')
def info():
    d = {
        "indigo_version": indigo.version(),
        "imago_versions": ["2.0.0", ],
    }
    return jsonify(d)


# TODO Not sure what it suppose to be
@bp.route('/indigo/calculate_cip', methods=['POST', ])
@load_molecule_from_request
def calculate_cip(mol=None):
    mol.markEitherCisTrans()
    mol.markStereobonds()
    d = {'struct': mol.molfile()}
    return jsonify(d)


@bp.route('/indigo/calculate', methods=['POST', ])
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
@bp.route('/indigo/check', methods=['POST', ])
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


@bp.route('/indigo/aromatize', methods=['POST', ])
@load_molecule_from_request
def aromatize(mol=None):
    mol.aromatize()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@bp.route('/indigo/dearomatize', methods=['POST', ])
@load_molecule_from_request
def dearomatize(mol=None):
    mol.dearomatize()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@bp.route('/indigo/layout', methods=['POST', ])
@load_molecule_from_request
def layout(mol=None):
    mol.layout()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


@bp.route('/indigo/clean', methods=['POST', ])
@load_molecule_from_request
def clean(mol=None):
    mol.clean2d()
    d = {
        'struct': mol.molfile(),
    }
    return jsonify(d)


# TODO
@bp.route('/imago/uploads', methods=['POST', ])
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
@bp.route('/imago/uploads/<file_id>', methods=['GET', ])
def recognize(file_id):
    fp = path.join(app.root_path, app.config['UPLOAD_FOLDER'], file_id)
    d = {
        "state": "SUCCESS",
        "metadata": {"mol_str": ""},
    }
    return jsonify(d)

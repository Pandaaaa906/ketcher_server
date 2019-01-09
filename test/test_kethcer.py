from flask import Flask, redirect, url_for
from ketcher import ketcher

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('ketcher.demo'))


if __name__ == '__main__':
    app.register_blueprint(ketcher.bp)
    app.run()

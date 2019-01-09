from flask import Flask, render_template
from flask_ketcher import ketcher


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def demo():
    return render_template("demo.html")


if __name__ == '__main__':
    app.register_blueprint(ketcher.bp)
    app.run()

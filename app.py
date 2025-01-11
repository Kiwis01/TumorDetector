from flask import Flask, request, render_template, url_for, redirect
import os
import urllib.request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def index():
    return render_template("index.html", upload=None)

@app.route("/", methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("index.html", filename=filename)
    return render_template("index.html", upload=None)

@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # For debugging



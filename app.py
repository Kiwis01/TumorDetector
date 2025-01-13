from flask import Flask, request, render_template, url_for, redirect
import os
import urllib.request
from werkzeug.utils import secure_filename
from PIL import Image
import os
import subprocess
import glob

app = Flask(__name__)

# Check if the folder exists
if not os.path.exists("./yolov5"):
    result = subprocess.run(["git", "clone", "https://github.com/ultralytics/yolov5"], capture_output=True, text=True)
    print(result.stdout)  # Print the output for debugging

# App utils
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/predict/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Function to validate allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_old_predictions(directory):
    files = glob.glob(directory + "/*")
    for f in files:
        os.remove(f)

# main page
@app.route("/")
def index():
    clear_old_predictions(app.config['RESULT_FOLDER'])
    return render_template("index.html", predicted=None)

# file upload call
@app.route("/", methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        predicted_image = prediction(filepath)
        if predicted_image:
            return render_template("index.html",predicted=predicted_image)
    return render_template("index.html", upload=None, predicted=None)

def prediction(filepath):
    # Clear old predictions
    clear_old_predictions(app.config['RESULT_FOLDER'])

    # yolov5 detect.py call
    command = [
        "python", "./yolov5/detect.py",
        "--weights", "./yolov5/runs/train/exp3/weights/best.pt",
        "--img", "640",
        "--conf", "0.60",
        "--source", filepath,
        "--project", "static/predict",
        "--name", "results",
        "--exist-ok"
    ]

    # Run the command
    subprocess.run(command, capture_output=True, text=True)

    # Update result image
    results_dir = os.path.join(app.config['RESULT_FOLDER'])

    # Ensure the directory exists and contains files
    if os.path.exists(results_dir) and os.listdir(results_dir):
        # Get the latest file based on modification time
        latest_file = max(
            [os.path.join(results_dir, f) for f in os.listdir(results_dir)],
            key=os.path.getmtime
        )
        # Ensure the latest file exists
        if os.path.exists(latest_file):
            return os.path.relpath(latest_file, 'static')  # Return the file path relative to the 'static' folder

# display prediction
@app.route("/display/<path:predicted>")
def display_image(predicted):
    # Ensure path joins with static folder
    return redirect(url_for('static', filename=f"static/predict/{predicted}"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)  # For debugging




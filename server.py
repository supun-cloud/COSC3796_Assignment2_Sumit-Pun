import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template with 30-second auto-refresh
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Screenshot Incommings</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: sans-serif; background: #333; color: white; text-align: center; }
        .gallery { display: flex; flex-wrap: wrap; justify-content: center; }
        .card { margin: 10px; background: #444; padding: 5px; border-radius: 5px; }
        img { max-width: 400px; height: auto; border: 1px solid #ccc; }
        p { margin: 5px 0; font-size: 0.8em; color: #aaa; }
    </style>
</head>
<body>
    <h1>Captured Screenshots</h1>
    <div class="gallery">
        {% for image in images %}
            <div class="card">
                <p>{{ image }}</p>
                <img src="{{ url_for('static', filename='uploads/' + image) }}">
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    
    try:
        images = sorted(os.listdir(UPLOAD_FOLDER), key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    except:
        images = []
    return render_template_string(HTML_TEMPLATE, images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    print(f"[+] Server received: {file.filename}")
    return "Success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
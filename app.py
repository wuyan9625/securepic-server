from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from utils import generate_id

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file_id = generate_id()
            filename = file_id + '.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            view_url = f'/view?id={file_id}'
            return render_template('upload_success.html', view_url=view_url)
    return render_template('upload.html')

@app.route('/view')
def view_image():
    image_id = request.args.get('id')
    if not image_id:
        return "No image ID provided.", 400
    filename = image_id + '.jpg'
    return render_template('view.html', filename=filename)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

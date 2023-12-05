from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

with open('keywords.txt', 'r') as keyword_file:
    filenames = keyword_file.read().splitlines()
    available_files = {filename: [] for filename in filenames if os.path.isfile(os.path.join('uploads', filename))}

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        # Update keywords.txt with filenames from the uploads folder
        files_in_uploads = os.listdir(UPLOAD_FOLDER)
        with open('keywords.txt', 'w') as keyword_file:
            keyword_file.write('\n'.join(files_in_uploads))
        
        return 'File uploaded successfully'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/available_files', methods=['GET'])
def get_available_files():
    return jsonify(list(available_files.keys()))

@app.route('/keywords', methods=['GET'])
def get_keywords():
    keywords = set()
    for file_keywords in available_files.values():
        keywords.update(file_keywords)
    return jsonify(list(keywords))


if __name__ == '__main__':
    app.run(debug=True)

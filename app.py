from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

available_files = {
    'file1.txt': ['keyword1', 'keyword2'],
    'file2.pdf': ['keyword3', 'keyword4'],
    # Add more files and keywords as needed
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        # Update available files with keywords when a new file is uploaded
        available_files[file.filename] = ['keyword_example']
        
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

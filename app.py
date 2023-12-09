from flask import Flask, request, send_file, jsonify
import io
import boto3

app = Flask(__name__)

# Initialize S3 client
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='',
    aws_secret_access_key=''
)

bucket_name = 'cs3800storage'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file_content = file.read()
        s3.put_object(Body=file_content, Bucket=bucket_name, Key=file.filename)
        
        return 'File uploaded successfully'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file = s3.get_object(Bucket=bucket_name, Key=filename)
        file_content = file['Body'].read()

        return send_file(
            io.BytesIO(file_content),
            attachment_filename=filename,
            as_attachment=True
        )
    except Exception as e:
        return str(e), 404

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        s3.delete_object(Bucket=bucket_name, Key=filename)
        return 'File deleted successfully', 200
    except Exception as e:
        return str(e), 500


@app.route('/available_files', methods=['GET'])
def get_available_files():
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)

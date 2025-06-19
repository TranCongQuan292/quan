# app.py
from flask import Flask, render_template, request, send_file
from rsa_utils import generate_keys, sign_data
import os
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

pubkey, privkey = generate_keys()

def send_signed_file(filepath, host='127.0.0.1', port=8888):
    with open(filepath, 'rb') as f:
        data = f.read()
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall(len(data).to_bytes(8, 'big'))
        s.sendall(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    action = request.form['action']

    if uploaded_file.filename == '':
        return "No file selected"

    filename = uploaded_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(filepath)

    with open(filepath, 'rb') as f:
        file_data = f.read()

    signature = sign_data(file_data, privkey)
    signed_path = filepath + '.signed'
    with open(signed_path, 'wb') as f:
        f.write(signature)

    if action == "download":
        return send_file(signed_path, as_attachment=True)
    elif action == "socket":
        try:
            send_signed_file(signed_path)
            return "Đã gửi file ký số qua socket thành công!"
        except Exception as e:
            return f"Lỗi khi gửi file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

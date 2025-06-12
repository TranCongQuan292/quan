from flask import Flask, render_template, request
from utils import generate_keys, sign_data, verify_signature
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

PRIVATE_KEY, PUBLIC_KEY = generate_keys()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sender')
def sender_page():
    return render_template('sender.html')

@app.route('/receiver')
def receiver_page():
    return render_template('receiver.html')

@app.route('/sign', methods=['POST'])
def sign():
    file = request.files['file']
    data = file.read()
    signature = sign_data(data, PRIVATE_KEY)

    # Lưu file
    with open(os.path.join(UPLOAD_FOLDER, 'file.bin'), 'wb') as f:
        f.write(data)
    with open(os.path.join(UPLOAD_FOLDER, 'signature.sig'), 'wb') as f:
        f.write(signature)
    with open(os.path.join(UPLOAD_FOLDER, 'public.pem'), 'wb') as f:
        f.write(PUBLIC_KEY)

    return render_template('sender.html', signature=True)

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files['file']
    signature = request.files['signature']
    publickey = request.files['publickey']
    result = verify_signature(file.read(), signature.read(), publickey.read())
    return render_template('receiver.html', result="Hợp lệ ✅" if result else "Không hợp lệ ❌")

if __name__ == '__main__':
    app.run(debug=True)

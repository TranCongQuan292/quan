from flask import Flask, render_template, request, send_file
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import io

app = Flask(__name__)

# Hàm tạo đối tượng AES
def get_aes_cipher(key_str, iv=None):
    key = key_str.encode('utf-8')
    if len(key) < 16:
        key = key.ljust(16, b'0')  # Bổ sung nếu thiếu
    else:
        key = key[:16]  # Cắt nếu dài quá
    if iv:
        return AES.new(key, AES.MODE_CBC, iv)
    else:
        return AES.new(key, AES.MODE_CBC)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key')
        file = request.files.get('file')

        if not file or not key:
            return "⚠️ Vui lòng chọn file và nhập khóa!", 400

        file_bytes = file.read()
        filename = file.filename

        try:
            if action == 'encrypt':
                iv = get_random_bytes(16)  # Khởi tạo IV ngẫu nhiên
                cipher = get_aes_cipher(key, iv)
                encrypted = cipher.encrypt(pad(file_bytes, AES.block_size))
                result_bytes = iv + encrypted  # Gắn IV vào đầu file mã hóa
                output_filename = 'encrypted_' + filename

            elif action == 'decrypt':
                iv = file_bytes[:16]  # Tách IV từ đầu file
                encrypted_data = file_bytes[16:]
                cipher = get_aes_cipher(key, iv)
                result_bytes = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                output_filename = 'decrypted_' + filename

            else:
                return "❌ Hành động không hợp lệ!", 400

        except ValueError:
            return "❌ Giải mã thất bại: Sai khóa hoặc dữ liệu không hợp lệ.", 400

        return send_file(
            io.BytesIO(result_bytes),
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/octet-stream'
        )

    return render_template('aes.html')

if __name__ == '__main__':
    app.run(debug=True)

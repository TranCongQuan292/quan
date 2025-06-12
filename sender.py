import socket
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Đọc khóa riêng
with open("private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# Đọc file cần gửi
filename = "file.txt"
with open(filename, "rb") as f:
    file_data = f.read()

# Tạo hash và ký số
hash_obj = SHA256.new(file_data)
signature = pkcs1_15.new(private_key).sign(hash_obj)

# Tạo socket và gửi
s = socket.socket()
s.connect(("localhost", 9999))
s.send(len(file_data).to_bytes(4, 'big') + file_data)
s.send(len(signature).to_bytes(2, 'big') + signature)
s.close()
print("File và chữ ký đã được gửi.")

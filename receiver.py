import socket
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Đọc khóa công khai
with open("public.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

# Lắng nghe file đến
s = socket.socket()
s.bind(("localhost", 9999))
s.listen(1)
conn, addr = s.accept()

# Nhận file
length = int.from_bytes(conn.recv(4), 'big')
file_data = conn.recv(length)

# Nhận chữ ký
sig_len = int.from_bytes(conn.recv(2), 'big')
signature = conn.recv(sig_len)

# Kiểm tra chữ ký
hash_obj = SHA256.new(file_data)
try:
    pkcs1_15.new(public_key).verify(hash_obj, signature)
    print("✅ Chữ ký hợp lệ. File chưa bị sửa.")
except (ValueError, TypeError):
    print("❌ Chữ ký không hợp lệ!")

with open("received_file.txt", "wb") as f:
    f.write(file_data)

conn.close()
s.close()

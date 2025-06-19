# socket_receiver.py
import socket
import os

os.makedirs('received_file', exist_ok=True)

def receive_file(host='0.0.0.0', port=8888):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(1)
        print("Đang chờ file...")

        conn, addr = s.accept()
        with conn:
            print(f"Kết nối từ {addr}")
            length = int.from_bytes(conn.recv(8), 'big')
            data = b''
            while len(data) < length:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            with open('received_file/file_signed.signed', 'wb') as f:
                f.write(data)

            print("Đã nhận và lưu file vào thư mục 'received_file/'.")

receive_file()

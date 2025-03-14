import socket
import bcrypt

# Hàm xác thực người dùng sử dụng bcrypt
def authenticate_user(username, password):
    stored_hash = b"$2b$12$rt16D3fChpVGvZmKwf6hO7pUlTwvJodBHLyykqntNqz.KbZV7eR6W"
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True
    else:
        return False

# Tạo server STUN-like với xác thực người dùng
def start_stun_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Server STUN-like đang lắng nghe tại {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        client_ip, client_port = addr
        print(f"Nhận yêu cầu từ {client_ip}:{client_port}")

        if data:
            message = data.decode()
            if message.startswith("AUTH:"):
                try:
                    username, password = message[5:].split(':')
                    if authenticate_user(username, password):
                        response = f"Địa chỉ IP công cộng của bạn: {client_ip}, Cổng: {client_port}"
                    else:
                        response = "Xác thực thất bại"
                except Exception as e:
                    response = f"Lỗi trong yêu cầu: {str(e)}"
            else:
                response = "Yêu cầu không hợp lệ. Vui lòng gửi yêu cầu theo định dạng 'AUTH:username:password'"

            server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 3478

    start_stun_server(host, port)

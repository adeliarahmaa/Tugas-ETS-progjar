from socket import *
import socket
import logging
from concurrent.futures import ThreadPoolExecutor

from file_protocol import FileProtocol
fp = FileProtocol()

def proses_client(connection, address):
    try:
        while True:
            data = connection.recv(32)
            if data:
                d = data.decode()
                hasil = fp.proses_string(d)
                hasil = hasil + "\r\n\r\n"
                connection.sendall(hasil.encode())
            else:
                break
    except Exception as e:
        logging.warning(f"Exception: {str(e)}")
    finally:
        connection.close()

class Server:
    def __init__(self, ipaddress='0.0.0.0', port=6666, max_threads=10):
        self.ipinfo = (ipaddress, port)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.executor = ThreadPoolExecutor(max_workers=max_threads)

    def run(self):
        logging.warning(f"Server berjalan di IP {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(5)
        while True:
            connection, address = self.my_socket.accept()
            logging.warning(f"Ada koneksi dari {address}")
            self.executor.submit(proses_client, connection, address)

def main():
    svr = Server(ipaddress='0.0.0.0', port=6666)
    svr.run()

if __name__ == "__main__":
    main()

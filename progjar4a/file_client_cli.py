import socket
import json
import base64
import logging
from concurrent.futures import ThreadPoolExecutor

server_address = ('172.16.16.101', 6665)
logging.basicConfig(level=logging.WARNING)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"Connecting to {server_address}")
    try:
        logging.warning(f"Sending message")
        sock.sendall(command_str.encode())

        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        hasil = json.loads(data_received)
        logging.warning("Data received from server:")
        return hasil
    except:
        logging.warning("Error during data receiving")
        return False

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("== Daftar file ==")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
    else:
        print("Gagal")

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
    else:
        print("Gagal")

def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as file:
            isifile = base64.b64encode(file.read()).decode()
        command_str = f"upload {filename} {isifile}"
        hasil = send_command(command_str)
        if hasil and hasil['status'] == 'OK':
            print(f" File '{filename}' berhasil diupload")
        else:
            print(f" Gagal upload file: {filename}")
    except FileNotFoundError:
        print(f" File '{filename}' tidak ditemukan")

def remote_download(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
        print(f" File '{filename}' berhasil diunduh")
    else:
        print(f" Gagal mengunduh file: {filename}")


if __name__ == '__main__':
    server_address=(('172.16.16.101', 6665))
    file_target = 'donalbebek.jpg'

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(remote_list)
        executor.submit(remote_get, file_target)
        executor.submit(remote_upload, file_target)
        executor.submit(remote_download, file_target)

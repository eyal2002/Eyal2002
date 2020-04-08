# -*- coding: utf-8 -*-
import socket
# C:\PY\PR\client_pr.py


def main():
    """
    Add Documentation here
    """
    ser_ip = '192.168.1.22'
    # ser_ip = socket.gethostbyname(socket.gethostname())
    ser_sock = socket.socket()
    ser_sock.bind((ser_ip, 8820))
    ser_sock.listen(10)
    (cli, addres) = ser_sock.accept()
    # print(ser_sock.recv(1024))
    while True:
        data = input('msg to server\n')
        print(data)
        cli.send(data.encode())
        # print(ser_sock.recv(1024).decode("utf-8"))
        if data == 'exit':
            break


if __name__ == '__main__':
    main()
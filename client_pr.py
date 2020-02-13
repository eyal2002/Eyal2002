# -*- coding: utf-8 -*-
import socket
# C:\PY\PR\client_pr.py


def main():
    """
    Add Documentation here
    """
    log_status = 'lo'
    # server_ip = '172.20.5.34'
    server_ip = '127.0.0.1'
    # server_ip = '192.168.43.207'
    cli_socket = socket.socket()
    cli_socket.connect((server_ip, 8820))
    print(cli_socket.recv(1024))
    while True:
        data = input('msg to server\n')
        print(data)
        cli_socket.send(data.encode())
        print(cli_socket.recv(1024).decode("utf-8"))
        if data == 'exit':
            break


if __name__ == '__main__':
    main()
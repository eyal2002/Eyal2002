# -*- coding: utf-8 -*-
import socket


def main():
    """
    Add Documentation here
    """
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8820))
    print '1'
    my_socket.send(raw_input())
    data = my_socket.recv(1024)
    print 'The server sent: ' + data
    my_socket.close()


if __name__ == '__main__':
    main()
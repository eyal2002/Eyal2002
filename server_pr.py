# -*- coding: utf-8 -*-
import socket
import select
import sqlite3
# C:\PR\server_pr.py


def send_waiting_messages(w_list):
    """
    sends the waiting messages
    :param w_list:
    """
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in w_list:
            for client in w_list:
                if client is not client_socket:
                    client.send(data)
            messages_to_send.remove(message)


def sign_up(user_data):
    """
    this function gets a string with data about the user and creates a new account for him.
    :param user_data:
    """
    data = user_data.split(':')[1].split()
    try:
        # sets the sqlite3 and the required materials
        conn = sqlite3.connect('PR_DB.db')
        c = conn.cursor()
        # tries to set a new user' if failing to do the username already exists
        c.execute("INSERT INTO users VALUES ('{0}', '{1}', '1', '1', '')".format(data[0], data[1]))
        conn.commit()
        # prints the current users table
        c.execute("SELECT * FROM users")
        print(c.fetchall())

        # sends the outcome to te client
        current_socket.send(b'success')
        print('yes')
        activate_user(data[0])
    except sqlite3.IntegrityError:
        current_socket.send(b'fail')
        print('no')


def sign_in(user_data):
    """
    this function gets a string with data about the user and creates a new account for him.
    :param user_data:
    """
    try:
        # sets the sqlite3 and the required materials
        conn = sqlite3.connect('PR_DB.db')
        c = conn.cursor()
        # tries to find and match the username and password
        [username, password] = user_data.split(':')[1].split()
        c.execute("SELECT password FROM users WHERE user_name = '" + username + "'")
        # sends required message to user
        if c.fetchall()[0][0] == password:
            print('yes')
            current_socket.send(b'success')
            activate_user(username)

        else:
            print('no')
            current_socket.send(b'fail')
    except IndexError:
        print('no')
        current_socket.send(b'fail')


def activate_user(user_name):
    """
    sets a user who singed in or singed up as an active user.
    :param user_name:
    :return:
    """
    sock_to_name[str(current_socket)] = user_name
    name_to_sock[user_name] = current_socket


def deactivate_user():
    """
    removes a user who singed out or disconnected from being an active user.
    :param:
    :return:
    """
    open_client_sockets.remove(current_socket)
    try:
        name_to_sock.pop(sock_to_name.pop(str(current_socket)))
    except KeyError:
        print('not connected yet')


def lo_data_handle(user_data):
    """
    handles the data from logged out users.
    :param user_data:
    :return:
    """
    print('logged out handler')
    if user_data[3:5] == 'si':
        # directs to the sign in function.
        print('sing in function')
        sign_in(user_data)

    if user_data[3:5] == 'su':
        # directs to the sign up function.
        print('sing in function')
        sign_up(user_data)

    if user_data[3:5] == 'rq':
        # answer a request that is nor requires to be singed in.
        pass


def li_data_handle(user_data):
    """
    handles the data from logged in users.
    :param user_data:
    :return:
    """
    data = user_data[3:].split(':')
    command = data[0]
    data = data[1]
    conn = sqlite3.connect('PR_DB.db')
    c = conn.cursor()
    if command == 'set_custom':
        data = data.split
        c.execute("UPDATE users SET spaceship = {0}, shot = {1} "
                  "Where user_name = {2}".format(data[0], data[1], sock_to_name.get(current_socket)))
    if command == 'get_custom':
        c.execute("SELECT spaceship, shot FROM users WHERE user_name == '{0}'"
                  "".format(sock_to_name.get(str(current_socket))))
        ts = c.fetchall()[0]
        current_socket.send('{0} {1}'.format(ts[0], ts[1]).encode())
        print('sent')

    if command == '':
        pass
    if command == '':
        pass


def main():
    """
    Add Documentation here
    """
    # server setup
    ser_sock = socket.socket()
    ser_sock.bind((socket.gethostbyname(socket.gethostname()), 8820))
    ser_sock.listen(1)

    # database setup
    conn = sqlite3.connect('PR_DB.db')
    c = conn.cursor()
    try:
        c.execute("CREATE TABLE users ([user_name] text primary key, [password] text, [spaceship] txt,"
                  " [shot] txt, [friends] text)")
        conn.commit()
    except sqlite3.OperationalError:
        print('table already exist')

    # varibles
    global messages_to_send, name_to_sock, sock_to_name, open_client_sockets, current_socket
    open_client_sockets = []
    messages_to_send = []
    name_to_sock = {}
    sock_to_name = {}

    # main run loop
    while True:
        try:
            rlist, wlist, xlist = select.select([ser_sock] + open_client_sockets, [], [])
            for current_socket in rlist:
                # checks if the current socket is already connected
                if current_socket is ser_sock:
                    print('new client')
                    (new_socket, addres) = ser_sock.accept()
                    open_client_sockets.append(new_socket)
                    new_socket.send(b'Successfully joined the chat')
                else:
                    try:

                        # receives data from the current socket
                        data = current_socket.recv(1024).decode("utf-8")
                        print(data)

                        # handles data of a logged out user, lo => log out
                        if data[:2] == 'lo':
                            lo_data_handle(data)

                        # handles data of a logged in user, li => logged in
                        elif data[:2] == 'li':
                            li_data_handle(data)

                        elif data == 'exit':
                            open_client_sockets.remove(current_socket)
                            current_socket.send(b'disconnected')

                        else:
                            current_socket.send(b'no you')

                    except ConnectionResetError:
                        print('disconnected')
                        deactivate_user()
                    except:
                        raise
        except:
            print('error - main loop failed')
            raise
        send_waiting_messages(open_client_sockets)


if __name__ == '__main__':
    main()

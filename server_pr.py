# -*- coding: utf-8 -*-
import socket
import select
import sqlite3
# C:\PR\server_pr.py
open_client_sockets = []
messages_to_send = []
name_to_sock = {}
sock_to_name = {}
in_game_users = []
current_socket = socket.socket()


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
        print('sing up function')
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
    # Organizes the data and prepare the access to the data base
    print('logged in handler')
    data = user_data[3:].split(':')
    command = data[0]
    conn = sqlite3.connect('PR_DB.db')
    c = conn.cursor()
    print(command)

    # sets the players active load-out
    if command == 'set_custom':
        print(data[1])
        data[1] = data[1].split()
        c.execute("UPDATE users SET spaceship = '{0}', shot = '{1}' "
                  "WHERE user_name == '{2}'".format(data[1][0], data[1][1], sock_to_name.get(str(current_socket))))
        conn.commit()
        current_socket.send(b'done')
        print('sent')

    # sends the users active load-out
    elif command == 'get_custom':
        c.execute("SELECT spaceship, shot FROM users WHERE user_name == '{0}'"
                  "".format(sock_to_name.get(str(current_socket))))
        ts = c.fetchall()[0]
        print('{0} {1}'.format(ts[0], ts[1]))
        current_socket.send('{0} {1}'.format(ts[0], ts[1]).encode())
        print('done')

    # returns all string with all of the users friends and another one with all of his connected friends
    elif command == 'get_friends_lobby':
        a_u = name_to_sock.keys()  # active users
        print(a_u)
        c.execute("SELECT friends FROM users WHERE user_name == '{0}'".format(sock_to_name.get(str(current_socket))))
        my_friends = c.fetchall()[0][0][:-1]
        fil = ''
        connected_users = [sock_to_name.get(user) for user in open_client_sockets]
        for friend in my_friends.split():
            if friend in connected_users:
                fil += friend
        print('my friends: ' + my_friends)
        current_socket.send('{0}:{1}'.format(my_friends, fil).encode())

    # adds a user as a friend if he is not in the list already
    elif command == 'add_friend':
        c.execute("SELECT friends FROM users WHERE user_name == '{0}'".format(sock_to_name.get(str(current_socket))))
        my_friends = c.fetchall()
        print(my_friends)
        my_friends = my_friends[0][0]
        print(my_friends)
        if data[1] not in my_friends.split() or True:
            print('a')
            c.execute("UPDATE users SET friends = '{0}' WHERE user_name == '{1}'"
                      "".format(my_friends + data[1] + ' ', sock_to_name.get(str(current_socket))))
            conn.commit()
            print('done')
            current_socket.send(b'done')

    # sends all of the current users of the game
    elif command == 'get_c_user':
        msg = ' '.join([name for name in name_to_sock.keys()])
        msg.replace(sock_to_name.get(str(current_socket)), '')
        print(msg)
        current_socket.send(msg.encode())

    # sends all of the user names of the users
    elif command == 'get_all_user':
        c.execute("SELECT user_name FROM users")
        all_users = c.fetchall()
        all_users.remove((sock_to_name.get(str(current_socket)), ))
        all_users = ' '.join([name[0] for name in all_users])
        print(all_users)
        current_socket.send(all_users.encode())

    # send the invitation to a game to who you requested to among your contacts
    elif command == 'send_game':
        data = data[1].split
        name_to_sock.get(data[1]).send('pop:{0}:{1}'.format(data[0], sock_to_name.get(str(current_socket))))


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

    # variables
    global messages_to_send, name_to_sock, sock_to_name, open_client_sockets, current_socket, in_game_users
    open_client_sockets = []
    in_game_users = []
    messages_to_send = []
    name_to_sock = {}
    sock_to_name = {}
    waiting_player = ''

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

                        elif data[:2] == 'pl':
                            if waiting_player == '':
                                waiting_player = data.split(':')[1]
                            else:
                                current_socket.send(waiting_player.encode())
                                name_to_sock.get(waiting_player.split()[1]).send(data.split(':')[1].encode())

                        elif data[:6] == 'cancel':
                            if sock_to_name.get(str(current_socket)) in waiting_player:
                                waiting_player = ''
                            else:
                                name_to_sock.get(data.split(':')).send(b'cancel')

                        else:
                            current_socket.send(b'no you')

                    except ConnectionResetError or ConnectionAbortedError:
                        print('disconnected')
                        deactivate_user()
        except ConnectionAbortedError:
            print('error - main loop failed')
            raise
        send_waiting_messages(open_client_sockets)


if __name__ == '__main__':
    main()

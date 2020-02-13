import socket
import select
import tkMessageBox
import sqlite3
import hashlib
import time

server_socket = socket.socket()
server_socket.bind(('0.0.0.0',1048))
server_socket.listen(5)
open_client_sockets=[]
messages_to_send_private=[]
messages_to_send_groups=[]
connected_clients_dict={}

def users_insert(username,password): #the function insert new row to usersDb table
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    #print "INSERT INTO usersDb VALUES ('"+username+"','"+password+"')"
    c.execute("INSERT INTO usersDb VALUES ('"+username+"','"+password+"')")
    conn.commit()
    #c.execute("SELECT * FROM usersDb WHERE username='"+username+"'")
    #print(c.fetchall())

def users_read(nameOrPass,var): #the function return the required row from usersDb table
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    c.execute("SELECT * FROM usersDb WHERE "+nameOrPass+"='"+var+"'")
    return (c.fetchall())





def users_cursor(): #the function creates new table in users.db
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
   # c.execute("""CREATE TABLE usersDb(
  #          username text,
 #           password text
#            )""")
    c.execute("INSERT INTO usersDb VALUES ('yarivd','25d55ad283aa400af464c76d713c07ad')")
    conn.commit()
    c.execute("SELECT * FROM usersDb WHERE username='yarivd'")
    print (c.fetchall())

def groups_insert(username,group_name): #the function insert new row to groupsDb table
    conn=sqlite3.connect('groups.db')
    c=conn.cursor()
    c.execute("INSERT INTO groupsDb VALUES ('"+username+"','"+group_name+"')")
    conn.commit()

def groups_read(group_or_username,var): #the function return the required row from groupsDb table
    conn=sqlite3.connect('groups.db')
    c=conn.cursor()
    c.execute("SELECT * FROM groupsDb WHERE "+group_or_username+"='"+var+"'")
    return (c.fetchall())


def groups_cursor(): #the function creates new table in groups.db
    conn=sqlite3.connect('groups.db')
    c=conn.cursor()
    #c.execute("""CREATE TABLE groupsDb(
    #        username text,
    #        group_name text
    #        )""")
    #c.execute("INSERT INTO groupsDb VALUES ('yarivd','25d55ad283aa400af464c76d713c07ad')")
    #conn.commit()
    #c.execute("SELECT * FROM groupsDb WHERE username='yarivd'")
    #print (c.fetchall())

def log_in(username,password): ##the function gets username, password and checks them
    check1=users_read("username",username)
    if not check1:
        print "this username doesn't exist"
        #label_3 = Label(root, text="this username doesn't exist",width=40,bg= "white",font=("bold", 10))
        #label_3.place(x=80,y=130)
        #tkMessageBox.showerror("error","this username doesn't exist")
        return False
    else:
        new=hashlib.md5(password).hexdigest()
        check2=users_read("password",new)
        if not check2:
            #tkMessageBox.showerror("error","wrong password")
            return False
        else:
            check1=check1[0]
            ans=False
            for user in check2:
                if user==check1:
                    ans=True
                    break
            if not ans:
                #tkMessageBox.showerror("error","wrong password")
                return False
            else:
                #tkMessageBox.showinfo("info","correct!")
                return True

def new_user(username,password): ##the function add new user to the users.db
    check1 = users_read("username", username)
    if check1:
        return False
    else:
        new = hashlib.md5(password).hexdigest()
        users_insert(username, new)
        return True


def send_waiting_messages_to_everyone(wlist): #send all the messages that are in the list of "messages_to_send"
    for message in messages_to_send:
        (client_socket,data)=message
        name=connected_clients_dict[client_socket]
        if client_socket in open_client_sockets:
            for client in wlist:
                if client_socket != client:
                    client.send(name+" sent: "+data)
                else:
                    client.send("you sent: "+data)
        messages_to_send.remove(message)


def send_waiting_messages_private(wlist): ##the function sends privates messages
    for message in messages_to_send_private:
        (name,data,current_socket)=message
        socket=None
        if " -pri_mess" in name:
            private = True
            #current_socket.send(data)
            index=name.find(" ")
            name=name[:index]
            data2=data.split(" ")
            if data2[0]=="*photo*":
                mess="*photo* "+connected_clients_dict[current_socket]+" "+data2[1]
            else:
                mess=data
        else:
            private = False

        for key in connected_clients_dict.keys():
            if connected_clients_dict[key]==name:
                socket=key


        if socket!=None and not private:
            #print name
            socket.send(connected_clients_dict[current_socket] + ": " + data)
        elif socket!=None:
            print 433
            time.sleep(0.3)
            socket.sendall(mess)
        messages_to_send_private.remove(message)

def send_waiting_messages_group(wlist): ##the function send groups messages
    for message in messages_to_send_groups:
        (name,data,current_socket)=message
        socket=None
        print name
        group_name=name
        if " -pri_mess" in name:
            index=group_name.find(" ")
            print group_name
            group_name=group_name[:index]
            print group_name
            print 77
            private = True
            index = name.find(" ")
            #group_name = group_name[:index]
            list_tuple = groups_read("group_name", group_name)
            list_name = []
            print list_tuple
            for tuple in list_tuple:
                list_name.append(tuple[0])
            list_socket=[]
            for key in connected_clients_dict.keys():
                if connected_clients_dict[key] in list_name:
                    list_socket.append(key)
            print list_socket
            #current_socket.send(data)
            data2=data.split(" ")
            if data2[0]=="*photo*":
                mess="*photo* group "+group_name+" "+connected_clients_dict[current_socket]+" "+data2[1]
            else:
                mess=data
        else:
            group_name = name[1:]
            list_tuple = groups_read("group_name", group_name)
            list_name = []
            for tuple in list_tuple:
                list_name.append(tuple[0])
            list_socket = []
            for key in connected_clients_dict.keys():
                if connected_clients_dict[key] in list_name:
                    list_socket.append(key)
            private = False


        print 99
        if len(list_socket)!=0 and not private:
            print 88
            for socket in list_socket:
                print 66
                if socket!=current_socket:
                    socket.send(group_name+": "+connected_clients_dict[current_socket] + ": " + data)
        elif len(list_socket)!=0:
            print 11
            for socket in list_socket:
                print 33
                if socket != current_socket:
                    print 44
                    socket.sendall(mess)
        else:
            print 22
        messages_to_send_groups.remove(message)

def receive_photo(client_socket, count):

    '''This function gets length of data and
    receive only the requested data.
    (for ex. if the data length is 10 the function
     receives 10 ?bytes? from client)'''

    buf = b''
    print '%%%%%'
    print count
    print '*******'
    print int(count)

    count=int(count)
    while count:
        new_buf = client_socket.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf

def main(): ##the main function which manages the chat
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                try:
                    cond = False
                    data = current_socket.recv(1024)
                except:
                    cond=True
                if cond or data=="":
                    open_client_sockets.remove(current_socket)
                    if current_socket in connected_clients_dict:
                        del connected_clients_dict[current_socket]
                else:
                    data2=data.split(" ")
                    if data2[0]=="*log_in:*":
                        ans=log_in(data2[1],data2[2])
                        connected_clients_dict[current_socket]=data2[1]
                        current_socket.send(str(ans))
                    elif data2[0]=="*sign_in:*":
                        ans=new_user(data2[1],data2[2])
                        connected_clients_dict[current_socket] = data2[1]
                        current_socket.send(str(ans))
                    elif data2[0]=="*who_connected:*":
                        ans=" "
                        for key in connected_clients_dict.keys():
                            if key!=current_socket:
                                ans=ans+connected_clients_dict[key]+","
                        print ans
                        print connected_clients_dict[current_socket]+"!!!"
                        if ans==" ":
                            current_socket.send(ans)
                        else:
                            current_socket.send(ans[1:])
                    elif data2[0]=="*photo*":
                        name=data2[1]
                        if data2[1]=="group":
                            name=data2[2]
                            size=data2[3]
                            photo = receive_photo(current_socket, size)
                            print name+" ****"
                            messages_to_send_groups.append((name + " -pri_mess", "*photo* " + size, current_socket))
                            send_waiting_messages_group(wlist)
                            messages_to_send_groups.append((name + " -pri_mess", photo, current_socket))
                        else:
                            size = data2[2]
                            print data2
                            photo = receive_photo(current_socket, size)
                            messages_to_send_private.append((name + " -pri_mess", "*photo* " + size, current_socket))
                            send_waiting_messages_private(wlist)
                            messages_to_send_private.append((name + " -pri_mess", photo, current_socket))
                    elif data2[0]=="*groups:*":
                        name=connected_clients_dict[current_socket]
                        list_db=groups_read("username", name)
                        list_groups=" "
                        for row in list_db:
                            group_name=row[1]
                            list_groups=list_groups+group_name+","
                        if list_groups==" ":
                            current_socket.send(list_groups)
                        else:
                            current_socket.send(list_groups[1:])
                    elif data2[0]=="*new_group*":
                        print data2[1]
                        print data2[2]
                        members=data2[2][:-1]
                        list_members=members.split(",")
                        if len(groups_read("group_name",data2[1]))>0:
                            current_socket.send("False")
                        else:
                            for member in list_members:
                                groups_insert(member,data2[1])
                            current_socket.send("True")
                    else:
                        index=data.find("*")
                        if "group " in data[:index]:
                            index2=data.find(" ")
                            messages_to_send_groups.append((data[index2:index],data[index+1:],current_socket))
                        else:
                            messages_to_send_private.append((data[:index],data[index+1:],current_socket))
                        #messages_to_send.append((current_socket,data))
            #print messages_to_send
            send_waiting_messages_private(wlist)
            send_waiting_messages_group(wlist)
            #send_waiting_messages_to_everyone(wlist)



if __name__ == '__main__':
    main()
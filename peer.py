import socket
import threading 
import uuid
import time
import json
import pickle

import tkinter

#172.16.137.207 b
#172.16.136.239 a
#172.16.136.62 h

TCP_IP = '0.0.0.0'
TCP_PORT = 10000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


search_mode = False
broadcast_mode = False
send_message = ''

my_name = "Sam"

searchField = ''
followerField = ''
messageField = ''

received_message_list = ''
sent_message_list = ''
searched_message_list = ''
log = ''


follower_connections = []
following_connections = []
following_threads = []
follower_threads = []

my_uuid = uuid.uuid1()
print(my_name + ": " + str(my_uuid))

received_messages_uuid = []
sent_messages_uuid = []
my_messages = []
query_conn = {}

def follow_new_peer():
    global send_message
    global broadcast_mode
    global followings_IP_list
    global following_connections, following_threads

    TCP_IP = followerField.get()
    TCP_PORT = 10000
    log.insert(0, "connecting to {}:{}".format(TCP_IP,TCP_PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    log.insert(0, "connected to {}:{}".format(TCP_IP,TCP_PORT))

    following_connections.append(s)

    followings_IP_list.insert(0, TCP_IP) # add to UI following list
    th = threading.Thread(target=following, args=(s,))
    th.start()

    following_threads.append(th)

def search_message():
    global send_message
    global search_mode
    global searchField
    global log
    
    log.insert(0, "searching for " + searchField.get())

    for message in my_messages:
        split_message = message.split(' ') 
        for word in split_message:
            if(word == searchField.get()):
                searched_message_list.insert(0, "myself" + " : " + message)

    log.insert(0, "search in followings for " + searchField.get())

    send_message = {
        'uuid': str(uuid.uuid1()),
        'type': 'query',
        'context': {
            'sender': my_name,
            'src': str(my_uuid),
            'text': searchField.get(),
            'time_stamp': time.time()
        }  
    }

    search_mode = True

def new_message():
    global send_message
    global broadcast_mode

    my_messages.append(messageField.get())

    log.insert(0, "sending new message: " + messageField.get())

    send_message = {
        'uuid': str(uuid.uuid1()),
        'type': 'broadcast',
        'context': {
            'sender': my_name,
            'src': str(my_uuid),
            'text': messageField.get(),
            'time_stamp': time.time()
        }  
    }

    broadcast_mode = True

def create():
    global followerField, messageField, searchField
    global received_message_list, sent_message_list, searched_message_list, followings_IP_list, followers_IP_list, log
    # global statusLabel
    global follower_connections, following_connections
    global follower_threads
    global following_threads

    def clear_bt():
        received_message_list.delete(0,'end')
        sent_message_list.delete(0,'end')
        searched_message_list.delete(0,'end')
    
    root = tkinter.Tk()

    def on_closing():
        for follower in follower_connections:
            follower.close()
        for following in following_connections:
            following.close()

        print('all connections are gone!!!')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # def set_status(status_value):
    #     global statusLabel
    #     statusLabel = tkinter.Label(root, text="status" + status_value).grid(row=3, column=2)


    received_message_list = tkinter.Listbox(root)
    sent_message_list = tkinter.Listbox(root)
    searched_message_list = tkinter.Listbox(root)
    followers_IP_list = tkinter.Listbox(root)
    followings_IP_list = tkinter.Listbox(root)
    log = tkinter.Listbox(root)

    root.title("Network")

    tkinter.Label(root, text='Recieved').grid(row=0, column=0) 
    tkinter.Label(root, text='Sent').grid(row=0, column=1) 
    tkinter.Label(root, text='Search').grid(row=0, column=2)
    tkinter.Label(root, text='Followers').grid(row=5, column=0)
    tkinter.Label(root, text='Followings').grid(row=5, column=1)
    tkinter.Label(root, text='log').grid(row=7, column=1)

    # statusLabel = tkinter.Label(root, text="status").grid(row=3, column=2)

    received_message_list.grid(row=1, column=0)
    sent_message_list.grid(row=1, column=1)
    searched_message_list.grid(row=1, column=2)

    followerField = tkinter.Entry(root)
    messageField = tkinter.Entry(root)
    searchField = tkinter.Entry(root)

    followerField.insert(0, '172.16.136.239')
    messageField.insert(0, 'message')
    searchField.insert(0, 'search')


    followButton = tkinter.Button(root, text='follow', width=10, command=follow_new_peer, highlightbackground='#3E4149')
    sendButton = tkinter.Button(root, text='send', width=10, command=new_message, highlightbackground='#3E4149')
    searchButton = tkinter.Button(root, text='search', width=10, command=search_message, highlightbackground='#3E4149')
    clearButton = tkinter.Button(root, text='clear', width=10, command=clear_bt, highlightbackground='#3E4149')

    clearButton.grid(row=2, column=2)

    followerField.grid(row=2, column=0)
    followButton.grid(row=2, column=1)
    
    messageField.grid(row=3, column=0)
    sendButton.grid(row=3, column=1)

    searchField.grid(row=4, column=0)
    searchButton.grid(row=4, column=1)

    followers_IP_list.grid(row=6, column=0)
    followings_IP_list.grid(row=6, column=1)

    log.grid(row=8, columnspan=3, sticky='WE')
    log.grid_columnconfigure(3,weight=3)

    root.mainloop()

def following_message(conn):
    global search_mode
    global query_conn
    global send_message

    while (True):
        data = conn.recv(BUFFER_SIZE)
        data = json.loads(data.decode())

        if (data['type'] == 'control'):
            log.insert(0, data['context']['text'] + ' from ' + data['context']['sender'])
        elif (data['type'] == 'query'):
            log.insert(0, 'search message received word: {} from: {}'.format(data['context']['text'], data['context']['sender']))
            
            send_message = data
            search_mode = True
            log.insert(0, "send search query to followings")
            
            query_conn[str(data['context']['src'])] = conn
            log.insert(0, 'searching for word: {}'.format(data['context']['text']))
            for message in my_messages:
                splited_message = message.split(' ')
                for word in splited_message:
                    if (data['context']['text'] == word):
                        send_message = {
                            'uuid': str(uuid.uuid1()),
                            'type': 'query_answer',
                            'context': {
                                'sender': my_name,
                                'src': str(my_uuid),
                                'rcv': data['context']['src'],
                                'text': message,
                                'time_stamp': time.time()
                            }  
                        }

                        conn.send((json.dumps(send_message)).encode())


def follower(conn):
    global broadcast_mode
    global send_message
    global sent_message_list

    threading.Thread(target=following_message, args=(conn,)).start()

    log.insert(0, "you have one new follower")

    while True:  
        if (broadcast_mode):
            sent_messages_uuid.insert(0, send_message['uuid'])
            sent_message_list.insert(0, send_message['context']['text'])
            conn.send((json.dumps(send_message)).encode())
            time.sleep(0.05)
            broadcast_mode = False
        else:
            time.sleep(0.001)
    
def search_thread(s):
    global search_mode
    global send_message

    while True:
        if (search_mode):
            s.send((json.dumps(send_message)).encode())
            time.sleep(0.05)
            search_mode = False
        else:
            time.sleep(0.001)

def following(s):
    global send_message
    global broadcast_mode
    global BUFFER_SIZE
    global received_message_list

    threading.Thread(target=search_thread, args=(s,)).start()

    while True: 
        data = s.recv(BUFFER_SIZE)
        data = json.loads(data.decode())
        
        log.insert(0, "you have one new message: {} type: {} ".format(data['context']['text'], data['type']))
        
        if (data['type'] == 'control'):
            print (data['context']['text']) # future work
        elif (data['type'] == 'query_answer'):
            if (data['context']['rcv'] == str(my_uuid)):
                searched_message_list.insert(0, data['context']['sender'] + " : " + data['context']['text'])
            else:
                try:
                    qconn = query_conn.get(str(data['context']['rcv']))
                    qconn.send(json.dumps(data).encode())                
                except:
                    pass
        elif (data['type'] == 'broadcast'):
            send_message = data
            rec_message_uuid = data['uuid']
            if (rec_message_uuid not in received_messages_uuid):
                received_messages_uuid.append(rec_message_uuid)
                received_message_list.insert(0, data['context']['sender'] + ": " +data['context']['text'])
                broadcast_mode = True
            else:
                log.insert(0, 'duplicated message received')                
                send_message = {
                    'uuid': str(uuid.uuid1()),
                    'type': 'control',
                    'context': {
                        'sender': my_name,
                        'src': str(my_uuid),
                        'text': 'duplicated message',
                        'time_stamp': time.time()
                    }  
                }

                s.send((json.dumps(send_message)).encode())


def connection():
    global followers_IP_list
    global follower_threads, follower_connections

    while True:
        conn, addr = s.accept()
        log.insert(0,'new connection address: '+ str(addr))
        follower_connections.append(conn)
        followers_IP_list.insert(0, addr)
        th = threading.Thread(target=follower, args=(conn,))
        th.start()
        follower_threads.append(th)
    conn.close()

threading.Thread(target=connection).start()
create()


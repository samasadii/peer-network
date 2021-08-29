import socket
import tkinter


def onClick():
    print("biiitch!!")

root = tkinter.Tk()

Lb1 = tkinter.Listbox(root)
Lb2 = tkinter.Listbox(root)

Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")

for i in range(1, 20):
    Lb2.insert(0,"item " + str(i))


root.title("Network")

tkinter.Label(root, text='Recieved').grid(row=0, column=0) 
tkinter.Label(root, text='Sent').grid(row=0, column=1) 

Lb1.grid(row=1, column=0)
Lb2.grid(row=1, column=1)

followerField = tkinter.Entry(root)
messageField = tkinter.Entry(root)

followerField.insert(0, 'IP')
messageField.insert(0, 'message')

followButton = tkinter.Button(root, text='follow', width=10, command=onClick, highlightbackground='#3E4149')
sendButton = tkinter.Button(root, text='send', width=10, command=root.destroy, highlightbackground='#3E4149')

#followButton = tkinter.Button(root, text='follow', width=10, command=root.destroy, bg='blue', fg='white')
#sendButton = tkinter.Button(root, text='send', width=10, command=root.destroy, bg='blue', fg='white')


followerField.grid(row=2, column=0)
followButton.grid(row=2, column=1)
messageField.grid(row=3, column=0)
sendButton.grid(row=3, column=1)

root.mainloop()

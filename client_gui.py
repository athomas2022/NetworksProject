from customtkinter import *
from CTkMessagebox import CTkMessagebox
import threading
import client
from queue import Queue
import os
import json


incoming = Queue()
contact_list = []
keyword = "gR33tinG$"


def refresh_contact_list():
    for wg in ContactScrollable.winfo_children():
        wg.destroy()
    for c in contact_list:
        cb = CTkButton(master=ContactScrollable, text=c, height=20)
        cb.pack(pady=(2, 2), fill='x')


def get_contacts():
    contact_list.clear()
    if not os.path.exists('contact_list.txt'):
        with open('contact_list.txt', 'w') as test:
            pass
    with open('contact_list.txt', 'r') as cl:
        for contact in cl:
            contact_list.append(contact)
    client.update_cc(len(contact_list))
    refresh_contact_list()


def write_contact(new_contact):
    if new_contact in contact_list or len(new_contact.strip()) == 0:
        return 1
    with open('contact_list.txt', 'a') as cl:
        cl.write(f'{new_contact}\n')
    get_contacts()
    return 0


def generate_message_text(md, clr):
    new_message = CTkTextbox(master=ChatScrollable, height=24 * (1 + (len(md) // 92)), wrap='word')
    new_message.insert('0.0', md)
    new_message.tag_config('sender_color', foreground=clr)
    new_message.tag_add('sender_color', '1.0', '1.4')
    new_message.configure(state='disabled')
    new_message.pack(fill='x')


def send_btn():
    msg_data = 'Me: ' + ChatEntry.get()
    if len(msg_data) > 4:
        print(msg_data)
        client.message_send(ChatEntry.get())
        generate_message_text(msg_data, 'red')
        ChatEntry.delete(0, len(msg_data))


def msg_recv():
    while True:
        external_msg = client.message_recv()
        if external_msg:
            incoming.put(external_msg)


def menu_gui():
    def add_contact(contact):
        write_contact(contact)
        ContactEntry.delete(0, len(contact))

    def is_disabled():
        if client.get_server_mode():
            return 'normal'
        return 'disabled'

    def server_connect(server_addr):
        client.update_server_mode(True)
        client.message_send(keyword, server_addr)
        ServerContactEntry.configure(state='normal', placeholder_text='Enter friendcode...')
        ServerContactBtn.configure(state='normal')

    def direct_connect():
        client.update_server_mode(False)
        ServerContactEntry.configure(state='disabled')
        ServerContactBtn.configure(state='disabled')


    menu_root = CTk()
    menu_root.title('Menu')
    menu_root.geometry('400x300')
    root.configure(fg_color=['gray92', 'gray14'])
    MenuFrame = CTkFrame(master=menu_root, width=400, height=300)
    MenuFrame.pack(side='top')
    MenuFrame.grid(column=0, row=0)
    ContactEntry = CTkEntry(master=MenuFrame, placeholder_text='Direct Connect with IP', width=300, height=50)
    ContactEntry.grid(column=0, row=0)
    ContactBtn = CTkButton(master=MenuFrame, text='Connect', width=100, height=50, command=direct_connect)
    ContactBtn.grid(column=1, row=0)
    ServerEntry = CTkEntry(master=MenuFrame, placeholder_text='Enter server IP...', width=300, height=50)
    ServerEntry.grid(column=0, row=1)
    ServerBtn = CTkButton(master=MenuFrame, text='Connect', width=100, height=50, command=lambda: server_connect(ServerEntry.get()))
    ServerBtn.grid(column=1, row=1)
    ServerContactEntry = CTkEntry(master=MenuFrame, placeholder_text='Enter friendcode...', width=300, height=50, state=is_disabled())
    ServerContactEntry.grid(column=0, row=2)
    ServerContactBtn = CTkButton(master=MenuFrame, text='Add', width=100, height=50, state=is_disabled())
    ServerContactBtn.grid(column=1, row=2)
    menu_root.mainloop()


recv_thread = threading.Thread(target=msg_recv, daemon=True)
recv_thread.start()

set_default_color_theme("dark-blue")

root = CTk()
root.title("A.Y.D.E.G.E.R.")
root.geometry("900x750")
root.configure(fg_color=['gray92', 'gray14'])

ChatFrame = CTkFrame(master=root, width=600, height=900)
ChatFrame.pack_propagate(False)
ChatFrame.pack(pady=(0, 0), side="right")
MenuBtn = CTkButton(master=ChatFrame, text='menu', command=menu_gui)
MenuBtn.pack(side='top')
ChatScrollable = CTkScrollableFrame(master=ChatFrame, orientation="vertical", width=200)
ChatScrollable.pack(pady=(0, 0), expand=1, fill="both")
ChatEntry = CTkEntry(master=ChatFrame, placeholder_text="Type message...", width=550, height=100)
ChatEntry.pack(side="left")
ChatSendButton = CTkButton(master=ChatFrame, text="Send", height=100, command=send_btn)
ChatSendButton.pack(side="right")
ContactFrame = CTkFrame(master=root, width=300, height=750)
ContactFrame.pack_propagate(False)
ContactFrame.pack(expand=1, side="left")
ContactScrollable = CTkScrollableFrame(master=ContactFrame, orientation="vertical")
ContactScrollable.pack(expand=1, fill="both")


def check_incoming():
    while not incoming.empty():
        msg = incoming.get()
        msg_json = json.loads(msg)
        if keyword in msg_json['message']:
            fc = msg_json['message'].replace(keyword, '').strip()
            CTkMessagebox(title='Successful server connection', message=f'Your server friendcode is {fc}')
        else:
            generate_message_text(msg, 'blue')
    root.after(100, check_incoming)


get_contacts()
check_incoming()
root.mainloop()

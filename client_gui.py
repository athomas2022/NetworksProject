from customtkinter import *
import client
class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ChatFrame = CTkFrame(master=self, width=600, height=900)
        self.ChatFrame.pack_propagate(False)
        self.ChatFrame.pack(pady=(50, 0), side="right")
        self.ChatScrollable = CTkScrollableFrame(master=self.ChatFrame, orientation="vertical", width=200)
        self.ChatScrollable.pack(pady=(0, 0), expand=1, fill="both")
        self.ChatEntry = CTkEntry(master=self.ChatFrame, placeholder_text="Type message...", width=550, height=100)
        self.ChatEntry.pack(side="left")
        self.ChatSendButton = CTkButton(master=self.ChatFrame, text="Send", height=100, command=self.send_btn)
        self.ChatSendButton.pack(side="right")
        self.ContactFrame = CTkFrame(master=self, width=300, height=750)
        self.ContactFrame.pack_propagate(False)
        self.ContactFrame.pack(expand=1, side="left")
        self.ContactScrollable = CTkScrollableFrame(master=self.ContactFrame, orientation="vertical")
        self.ContactScrollable.pack(expand=1, fill="both")

    def send_btn(self):
        msg_data = 'Me: ' + self.ChatEntry.get()
        if len(msg_data) > 0:
            print(msg_data)
            client.message_send(self.ChatEntry.get())
            new_message = CTkTextbox(master=self.ChatScrollable, height=24*(1+(len(msg_data)//92)), wrap='word')
            new_message.insert('0.0', msg_data)
            new_message.tag_config('sender_color', foreground='red')
            new_message.tag_add('sender_color', '1.0', '1.4')
            new_message.configure(state='disabled')
            new_message.pack(fill='x')
            self.ChatEntry.delete(0, len(msg_data))


set_default_color_theme("dark-blue")
root = App()
root.geometry("900x750")
root.title("Window")
root.configure(fg_color=['gray92', 'gray14'])
root.mainloop()


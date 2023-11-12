from tkinter import Tk, Frame
import customtkinter as ctk
import threading
from client import Client

ctk.set_appearance_mode('dark')

class Client_GUI:
    def __init__(self, root):
        self.window = root
        self.window.title('Chat Client')
        self.client = Client('localhost', 12345)

        self.main_frame = Frame(self.window, bg='#2e2e2e')
        self.main_frame.pack(fill='both', expand=True)

        self.init_username_interface()

    def init_username_interface(self):
        self.username_frame = Frame(self.main_frame, bg='#2e2e2e')
        self.username_frame.pack(fill='both', expand=True)

        self.username_label = ctk.CTkLabel(self.username_frame, text="Enter Username:")
        self.username_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.username_frame, width=300)
        self.username_entry.pack(pady=10)
        self.username_entry.bind('<Return>', lambda event: self.set_username())

        self.username_button = ctk.CTkButton(self.username_frame, text='OK', command=self.set_username)
        self.username_button.pack(pady=10)

    def set_username(self):
        self.username = self.username_entry.get()
        self.client.send_message(f"Username: {self.username}")

        self.username_frame.pack_forget()

        self.init_chat_interface()
        self.message_entry.focus_set()

    def init_chat_interface(self):
        self.chat_frame = Frame(self.main_frame, bg='#2e2e2e')
        self.chat_frame.pack(fill='both', expand=True)

        self.chat_box = ctk.CTkTextbox(self.chat_frame, state='disabled', width=800, height=300)
        self.chat_box.pack(pady=10)

        self.message_entry = ctk.CTkEntry(self.chat_frame, width=800)
        self.message_entry.pack(pady=10)
        self.message_entry.bind('<Return>', lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.chat_frame, text='Send', command=self.send_message)
        self.send_button.pack(pady=10, side='right')

        self.quit_button = ctk.CTkButton(self.chat_frame, text='Close Chat', command=self.window.quit)
        self.quit_button.pack(pady=10, side='left')

        thread = threading.Thread(target=self.check_for_messages)
        thread.daemon = True
        thread.start()

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.client.send_message(message)
            self.append_to_chat(f"{self.username}: {message}")
            self.message_entry.delete(0, 'end')

    def append_to_chat(self, message):
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"{message}\n")
        self.chat_box.configure(state='disabled')

    def check_for_messages(self):
        while True:
            message = self.client.receive_message()
            if message:
                message = message.decode()
                if ':' in message:
                    sender, message = message.split(':', 1)
                else:
                    sender = "Admin"
                self.append_to_chat(f"{sender}: {message}")

if __name__ == '__main__':
    root = Tk()
    app = Client_GUI(root)
    root.mainloop()

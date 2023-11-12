from multiprocessing import Process
from server import Server
from client_gui import Client_GUI
from tkinter import Tk
import customtkinter as ctk

def set_dark_theme():
    ctk.set_appearance_mode('dark')

def run_server():
    server = Server('localhost', 12345)
    server.handle_clients()

def run_client():
    set_dark_theme()
    root = Tk()
    app = Client_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    server_process = Process(target=run_server)
    client_process1 = Process(target=run_client)
    client_process2 = Process(target=run_client)

    server_process.start()
    client_process1.start()
    client_process2.start()

    server_process.join()
    client_process1.join()
    client_process2.join()

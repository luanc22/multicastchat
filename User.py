import json
import socket
import sys
import threading
import time
from datetime import date
import tkinter as tk
from tkinter import scrolledtext, messagebox

from Connection import handle_messages

try:
    # Initialize global variables
    SERVER_ADDRESS = ""
    SERVER_PORT = 0
    username = ""

    # Create a socket instance and connect to the server
    socket_instance = socket.socket()
    socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))

    # Start a thread to handle received messages
    threading.Thread(target=handle_messages, args=[socket_instance]).start()

    print('Connected to chat!')

    while True:
        msg = str(input("Digite a mensagem: "))
        time_raw = time.localtime()
        time_value = time.strftime("%H:%M:%S", time_raw)
        today = date.today()
        date_value = today.strftime("%d/%m/%Y")
        payload = {
            "username": username,
            "message": msg,
            "time": time_value,
            "date": date_value,
        }

        if msg == 'fechar':
            print("Saindo da sessao...")
            break

        payload = json.dumps(payload)

        socket_instance.send(bytes(payload, 'utf-8'))

    socket_instance.close()

except Exception as erro:
    print(f'Ocorreu um erro\n {erro}')
    socket_instance.close()

# Function to send a message
def send_message():
    message = message_entry.get()
    if message:
        time_raw = time.localtime()
        time_value = time.strftime("%H:%M:%S", time_raw)
        today = date.today()
        date_value = today.strftime("%d/%m/%Y")
        payload = {
            "username": username,
            "message": message,
            "time": time_value,
            "date": date_value,
        }
        payload = json.dumps(payload)
        try:
            socket_instance.send(bytes(payload, 'utf-8'))
            message_text.insert(tk.END, f'You > {message} \n {time_value} - {date_value}\n\n')
            message_text.see(tk.END)  # Scroll to the end of the text
        except Exception as e:
            print(f'Error sending message: {e}')
            messagebox.showerror("Error", "Failed to send message")
    message_entry.delete(0, tk.END)

def clear_text():
    message_text.delete(1.0, tk.END)  # Delete all text from the start to the end

# Redirect stdout and stderr to display in the GUI
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end of the text

# Create a tkinter window
window = tk.Tk()
window.title("Chat Client")
window.resizable(False, False)  # This makes it non-resizable in both dimensions

# Create a frame to contain the labels and entry widgets
input_frame = tk.Frame(window)
input_frame.pack(pady=5)

# Create labels and entry widgets for IP, Port, and Username with padding
ip_label = tk.Label(input_frame, text="Server IP:")
ip_label.grid(row=0, column=0, padx=5, pady=2)

ip_entry = tk.Entry(input_frame)
ip_entry.grid(row=0, column=1, padx=5, pady=2)

port_label = tk.Label(input_frame, text="Server Port:")
port_label.grid(row=1, column=0, padx=5, pady=2)

port_entry = tk.Entry(input_frame)
port_entry.grid(row=1, column=1, padx=5, pady=2)

username_label = tk.Label(input_frame, text="Username:")
username_label.grid(row=2, column=0, padx=5, pady=2)

username_entry = tk.Entry(input_frame)
username_entry.grid(row=2, column=1, padx=5, pady=2)

# Create a connect button with padding
def connect():
    global SERVER_ADDRESS, SERVER_PORT, username, socket_instance

    SERVER_ADDRESS = ip_entry.get()
    SERVER_PORT = int(port_entry.get())
    username = username_entry.get()

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        threading.Thread(target=handle_messages, args=[socket_instance]).start()
        connect_button.config(state=tk.DISABLED)
        messagebox.showinfo("Connected", "Connected to chat server!")
    except Exception as e:
        print(f'Error connecting to server: {e}')
        messagebox.showerror("Error", "Failed to connect to server")

connect_button = tk.Button(window, text="Connect", command=connect)
connect_button.pack(pady=10)

# Create a scrolled text area for displaying messages with padding
message_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
message_text.pack(padx=10, pady=5)

# Create a label for the typing area
message_label = tk.Label(window, text="Type your message:")
message_label.pack(side=tk.LEFT, padx=5)

# Create an Entry widget for typing messages with padding
message_entry = tk.Entry(window, width=40)
message_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame to contain the "Send" and "Clear" buttons side by side
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

# Create a "Send" button with padding and pack it to the left
send_button = tk.Button(button_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

# Create a "Clear" button with padding and pack it to the left
clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
clear_button.pack(side=tk.LEFT, padx=5)

# Redirect stdout and stderr to display in the GUI
sys.stdout = StdoutRedirector(message_text)
sys.stderr = StdoutRedirector(message_text)

# Start the tkinter main loop
window.mainloop()

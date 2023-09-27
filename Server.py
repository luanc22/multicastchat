import socket
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext
from Connection import connections, handle_user_connection, remove_connection


# Function to start the server (unchanged)
def start_server(port):
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', port))
        socket_instance.listen(4)

        print('Server running!')

        while True:
            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as erro:
        print(f'An error occurred\n{erro}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


# Create a tkinter window
window = tk.Tk()
window.title("Server GUI")

# Create a frame to contain the port label and entry side by side
port_frame = tk.Frame(window)
port_frame.pack(pady=5)

# Create a label for the port
port_label = tk.Label(port_frame, text="Port:")
port_label.grid(row=0, column=0, padx=5, pady=5)

# Create an Entry widget for the port
port_entry = tk.Entry(port_frame)
port_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a button to start the server
def start_server_button_clicked():
    port = int(port_entry.get())
    if port:
        threading.Thread(target=start_server, args=(port,)).start()

start_button = tk.Button(window, text="Start Server", command=start_server_button_clicked)
start_button.pack(pady=10)

# Create a scrolled text area with increased size
message_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=15)  # Adjust width and height as needed
message_text.pack(padx=10, pady=5)

# Redirect stdout to the Text widget
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end of the text

sys.stdout = StdoutRedirector(message_text)

# Start the tkinter main loop
window.mainloop()
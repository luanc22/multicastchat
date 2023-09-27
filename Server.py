import socket
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext
from Connection import connections, handle_user_connection, remove_connection


# Funcao para iniciar o servidor
def start_server(port):
    try:
        # Cria o sockets bindando a porta e entao fica ouvindo por conexões
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', port))
        socket_instance.listen(4)

        print(f'Server rodando no endereco 127.0.0.1:{port}')

        # Parte dos sockets que aceita as conexoes e linka aos clientes
        # Cria uma thread para cada nova conexao criada
        while True:
            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as error:
        print(f'An error occurred:\n{error}')
    finally:
        # Verifica se tem conexoes restantes, caso sim, fecha elas e libera a porta
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


# Configuracoes do Tkinter

# Janela
window = tk.Tk()
window.title("Servidor de Mensagens")
window.resizable(False, False)

# Frame dos entrys e das labels
port_frame = tk.Frame(window)
port_frame.pack(pady=5)

# Labels e entrys para as configuracoes do server
port_label = tk.Label(port_frame, text="Porta:")
port_label.grid(row=0, column=0, padx=5, pady=5)
port_entry = tk.Entry(port_frame)
port_entry.grid(row=0, column=1, padx=5, pady=5)

# Botao de iniciar o servidor
def start_server_button_clicked():
    port = int(port_entry.get())
    if port:
        threading.Thread(target=start_server, args=(port,)).start()

start_button = tk.Button(window, text="Iniciar servidor", command=start_server_button_clicked)
start_button.pack(pady=10)

# Area de texto e o scrollbar
message_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=15)  # Adjust width and height as needed
message_text.pack(padx=10, pady=5)

# Redireciona textos do console para a area de texto
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

sys.stdout = StdoutRedirector(message_text)

# Mantem a janela aberta em loop
window.mainloop()


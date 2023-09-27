import json
import socket
import sys
import threading
import time
from datetime import date
import tkinter as tk
from tkinter import scrolledtext, messagebox
from Connection import handle_messages

# Funcao para enviar a mensagem
def send_message():
    message = message_entry.get()
    if message:
        raw_time = time.localtime()
        time_value = time.strftime("%H:%M:%S", raw_time)
        today = date.today()
        date_value = today.strftime("%d/%m/%Y")

        # Cria o payload com o dicionario que carrega as variaveis
        payload = {
            "username": username,
            "message": message,
            "time": time_value,
            "date": date_value,
        }

        # Serialize em Json
        payload = json.dumps(payload)
        try:
            # Manda a mensagem pro servidor
            socket_instance.send(bytes(payload, 'utf-8'))

            # Exibe na area de texto a mensagem enviada
            message_text.insert(tk.END, f'You > {message} \n {time_value} - {date_value}\n\n')
            message_text.see(tk.END)
        except Exception as error:
            print(f'Error sending message: {error}')
            messagebox.showerror("Erro", "Erro ao enviar a mensagem")

    # Limpa o campo de escrever a mensagem
    message_entry.delete(0, tk.END)


# Funcao para limpar o historico de mensagens
def clear_text():
    message_text.delete(1.0, tk.END)


# Redireciona textos do console para a area de texto
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)


# Configuracoes do Tkinter

# Janela
window = tk.Tk()
window.title("Chat")
window.resizable(False, False)

# Frame dos entrys e das labels
input_frame = tk.Frame(window)
input_frame.pack(pady=5)

# Labels e entrys para as configuracoes de conexao com o server
ip_label = tk.Label(input_frame, text="IP do Server:")
ip_label.grid(row=0, column=0, padx=5, pady=2)
ip_entry = tk.Entry(input_frame)
ip_entry.grid(row=0, column=1, padx=5, pady=2)

port_label = tk.Label(input_frame, text="Porta do Servidor:")
port_label.grid(row=1, column=0, padx=5, pady=2)
port_entry = tk.Entry(input_frame)
port_entry.grid(row=1, column=1, padx=5, pady=2)

username_label = tk.Label(input_frame, text="Usuario:")
username_label.grid(row=2, column=0, padx=5, pady=2)
username_entry = tk.Entry(input_frame)
username_entry.grid(row=2, column=1, padx=5, pady=2)

# Botao de conexao que realiza a tentativa de conexao com o server
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
        messagebox.showinfo("Conectado", "Conectado ao servidor de mensagens")
    except Exception as error:
        print(f'Error connecting to server: {error}')
        messagebox.showerror("Erro", "Falha na conexao com o servidor")


connect_button = tk.Button(window, text="Conectar", command=connect)
connect_button.pack(pady=10)

# Area de texto e o scrollbar
message_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
message_text.pack(padx=10, pady=5)

# Label do texto de digitar
message_label = tk.Label(window, text="Digite sua mensagem:")
message_label.pack(side=tk.LEFT, padx=5)

# Entry para digitar a mensagem
message_entry = tk.Entry(window, width=40)
message_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Frame dos botoes
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

# Botao de enviar mensagem
send_button = tk.Button(button_frame, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

# Botao de limpar o texto
clear_button = tk.Button(button_frame, text="Limpar", command=clear_text)
clear_button.pack(side=tk.LEFT, padx=5)

# Redireciona mensagens de console para a area de texto
sys.stdout = StdoutRedirector(message_text)
sys.stderr = StdoutRedirector(message_text)

# Mantem a janela aberta em loop
window.mainloop()

import json
import socket

# Lista para armazenar as conexoes
connections = []


# Funcao que lida com as conexoes dos usuarios
def handle_user_connection(connection: socket.socket, address: str) -> None:
    """
    Essa funcao recebe e processa as mensagens recebidas pelos usuarios fazendo o broadcast para todos conectados.

    Args:
        connection (socket.socket): Socket de conexao do usuario.
        address (str): Ip e porta de endereco do usuario.
    """
    while True:
        try:
            message = connection.recv(1024)
            message_dumped = json.loads(message)

            if message:
                # Printa a mensagem recebida
                print(
                    f'\n{message_dumped["username"]}: {message_dumped["message"]}\n{message_dumped["time"]} - {message_dumped["date"]}')

                # Cria a mensagem a ser enviada no broadcast
                msg_to_send = f'\n{message_dumped["username"]}: {message_dumped["message"]}\n{message_dumped["time"]} - {message_dumped["date"]}'

                # Envia a mensagem para todos os usuarios conectados
                broadcast(msg_to_send, connection)
            else:
                # Se a mensagem for vazia, fecha a conexao e sai do loop
                remove_connection(connection)
                break

        except Exception as error:
            print(f'Error handling user connection: {error}')
            remove_connection(connection)
            break


# Funcao de broadcast para distribuir a mensagem
def broadcast(message: str, connection: socket.socket) -> None:
    """
    Envia a mensagem para todos os clientes conectados exceto quem esta enviando.

    Args:
        message (str): Mensagem a ser enviada
        connection (socket.socket): A conexao de quem esta enviando a mensagem
    """
    for client_connection in connections:
        if client_connection != connection:
            try:
                # Faz o envio da mensagem
                client_connection.send(message.encode())
            except Exception as error:
                print(f'Error broadcasting message: {error}')
                remove_connection(client_connection)


# Funcao para remover a conexao de um usuario
def remove_connection(connection: socket.socket) -> None:
    """
    Remove a conexao dos usuarios da lista de usuarios conectados

    Args:
        connection (socket.socket): A conexao a ser removida
    """
    if connection in connections:
        connection.close()
        connections.remove(connection)


# Funcao para lidar com as mensagens recebidas e enviar para a area de texto
def handle_messages(connection: socket.socket):
    """
    Gerencia as mensagens recebidas e as envia para a interface grafica

    Args:
        connection (socket.socket): O socket de conexao das mensagens recebidas
    """
    while True:
        try:
            message = connection.recv(1024)
            if message:
                # Printa a mensagem
                print(message.decode())
            else:
                # Se a mensagem for vazia, fecha a conexao e sai do loop
                connection.close()
                break

        except Exception as error:
            print(f'An error occurred: {error}')
            connection.close()
            break

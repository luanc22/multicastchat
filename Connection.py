import json
import socket

connections = []

# Function to handle user connections (unchanged)
def handle_user_connection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            msg = connection.recv(1024)
            msg_dumped = json.loads(msg)

            if msg:
                print(f'\n{msg_dumped["username"]} > {msg_dumped["message"]}\n{msg_dumped["time"]} - {msg_dumped["date"]}')

                msg_to_send = f'\n{msg_dumped["username"]} > {msg_dumped["message"]}\n{msg_dumped["time"]} - {msg_dumped["date"]}'
                broadcast(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error handling user connection: {e}')
            remove_connection(connection)
            break

# Function to broadcast messages (unchanged)
def broadcast(message: str, connection: socket.socket) -> None:
    for client_conn in connections:
        if client_conn != connection:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print(f'Error broadcasting message: {e}')
                remove_connection(client_conn)

# Function to remove a connection (unchanged)
def remove_connection(conn: socket.socket) -> None:
    if conn in connections:
        conn.close()
        connections.remove(conn)

# Function to handle received messages and display them in the GUI
def handle_messages(connection: socket.socket):
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())  # Print received messages to console (optional)
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Ocorreu um erro: {e}')
            connection.close()
            break


import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clientes = []
nombres = []

# Enviar mensaje a todos
def broadcast(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)

# Manejar cliente
def manejar_cliente(cliente):

    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast(mensaje)

        except:
            indice = clientes.index(cliente)

            clientes.remove(cliente)
            cliente.close()

            nombre = nombres[indice]
            nombres.remove(nombre)

            broadcast(f"{nombre} salió del chat.".encode())

            break

# Recibir conexiones
def recibir():

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.bind((HOST, PORT))

    servidor.listen()

    print(f"Servidor escuchando en puerto {PORT}")

    while True:

        cliente, direccion = servidor.accept()

        print(f"Conectado con {direccion}")

        cliente.send("NOMBRE".encode())

        nombre = cliente.recv(1024).decode()

        nombres.append(nombre)
        clientes.append(cliente)

        print(f"Nombre del usuario: {nombre}")

        broadcast(f"{nombre} entró al chat.".encode())

        cliente.send("Conectado al servidor.".encode())

        thread = threading.Thread(target=manejar_cliente, args=(cliente,))
        thread.start()

recibir()
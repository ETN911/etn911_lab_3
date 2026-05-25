import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

nombre = input("Tu nombre: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORT))

# Recibir mensajes
def recibir():

    while True:

        try:
            mensaje = cliente.recv(1024).decode()

            if mensaje == 'NOMBRE':
                cliente.send(nombre.encode())

            else:
                print(mensaje)

        except:
            print("Error de conexión")
            cliente.close()
            break

# Enviar mensajes
def escribir():

    while True:

        mensaje = f"{nombre}: {input('')}"

        cliente.send(mensaje.encode())

thread_recibir = threading.Thread(target=recibir)
thread_recibir.start()

thread_escribir = threading.Thread(target=escribir)
thread_escribir.start()
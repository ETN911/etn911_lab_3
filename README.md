# Guía Práctica de Sockets en Python  
## Chat interactivo multiusuario con nombres de usuario

Esta práctica te enseñará los fundamentos reales de redes usando sockets TCP.  
El objetivo es construir un pequeño sistema de chat donde:

- varios clientes se conectan al servidor,
- cada usuario elige un nombre,
- los mensajes aparecen identificados con ese nombre,
- todos los clientes reciben los mensajes en tiempo real.

Aprenderás:

- sockets TCP,
- conexiones cliente-servidor,
- multithreading,
- comunicación en red,
- broadcasting,
- manejo básico de usuarios.

---

# 1. Arquitectura del sistema

El sistema tendrá:

## Servidor
- Espera conexiones.
- Acepta múltiples clientes.
- Guarda sus nombres.
- Reenvía mensajes a todos.

## Clientes
- Se conectan al servidor.
- Envían su nombre.
- Pueden escribir mensajes.
- Reciben mensajes de otros usuarios.

---

# 2. Estructura de archivos

Crea una carpeta:

```bash
chat_sockets/
```

Dentro:

```text
chat_sockets/
│
├── servidor.py
└── cliente.py
```

---

# 3. Conceptos básicos

## Socket

Un socket es un extremo de comunicación entre procesos.

En TCP:

- servidor escucha,
- cliente se conecta,
- ambos envían bytes.

---

## Modelo TCP/IP

```text
Cliente -----> Servidor
```

TCP garantiza:

- entrega,
- orden,
- integridad.

---

# 4. El servidor

## Código completo — `servidor.py`

```python
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
```

---

# 5. Explicación detallada del servidor

## Crear socket

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- `AF_INET` → IPv4
- `SOCK_STREAM` → TCP

---

## bind()

```python
servidor.bind((HOST, PORT))
```

Asocia IP y puerto.

---

## listen()

```python
servidor.listen()
```

El servidor queda esperando conexiones.

---

## accept()

```python
cliente, direccion = servidor.accept()
```

Acepta clientes nuevos.

---

## recv()

```python
mensaje = cliente.recv(1024)
```

Lee datos.

---

## send()

```python
cliente.send(mensaje)
```

Envía datos.

---

## Threads

Cada cliente se maneja en un hilo independiente:

```python
threading.Thread(...)
```

Así varios usuarios pueden hablar simultáneamente.

---

# 6. Cliente

## Código completo — `cliente.py`

```python
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
```

---

# 7. Cómo ejecutar

## Terminal 1

Ejecuta el servidor:

```bash
python servidor.py
```

---

## Terminal 2

Primer cliente:

```bash
python cliente.py
```

---

## Terminal 3

Segundo cliente:

```bash
python cliente.py
```

---

# 8. Resultado esperado

## Cliente 1

```text
Tu nombre: Ana

Ana entró al chat.
Luis entró al chat.

Hola
Luis: Hola
```

---

## Cliente 2

```text
Tu nombre: Luis

Ana entró al chat.

Hola
Ana: Hola
```

---

# 9. Flujo real de red

Cuando escribes:

```text
Hola
```

ocurre:

```text
Cliente Ana
   ↓
Servidor
   ↓
Todos los clientes
```

---

# 10. Conceptos importantes aprendidos

## Comunicación bidireccional

Cliente y servidor pueden enviar/recibir simultáneamente.

---

## Broadcasting

El servidor redistribuye mensajes.

---

## Concurrencia

Cada cliente usa un hilo.

---

## TCP

Garantiza:
- orden,
- confiabilidad,
- retransmisión.

---

# 11. Mejoras posibles

## Nivel intermedio

### Mostrar usuarios conectados

```python
/usuarios
```

---

### Mensajes privados

```text
@Luis hola
```

---

### Comandos

```text
/salir
/help
```

---

## Nivel avanzado

### Interfaz gráfica

Usar:

- Tkinter
- PyQt

---

### Chat web

Usar:

- WebSockets
- Flask
- FastAPI

---

### Cifrado

Usar:

- TLS/SSL
- cryptography

---

### Base de datos

Guardar historial:

- SQLite
- PostgreSQL

---

# 12. Experimentos recomendados

## Cambiar IP

Prueba conexión entre dos PCs reales:

```python
HOST = '192.168.1.20'
```

---

## Usar Linux y Windows

Conecta ambos sistemas.

---

## Probar latencia

Agrega:

```python
import time
```

---

# 13. Qué estás aprendiendo realmente

Este ejercicio parece pequeño, pero introduce ideas fundamentales usadas en:

- Discord
- WhatsApp
- videojuegos online
- servidores web
- sistemas distribuidos
- microservicios
- brokers de mensajes

---

# 14. Problemas típicos

## Error:

```text
Address already in use
```

Puerto ocupado.

Solución:

Cambiar puerto o cerrar procesos.

---

## Firewall bloquea

Abrir el puerto en Windows Defender.

---

## Cliente no conecta

Verificar:

- IP correcta,
- mismo puerto,
- servidor ejecutándose.

---

# 15. Siguiente paso recomendado

Después de dominar esto:

1. sockets UDP,
2. protocolo HTTP,
3. WebSockets,
4. asyncio,
5. servidores concurrentes,
6. arquitectura cliente-servidor avanzada.

---

# 16. Ejercicio final

Implementa:

## Sistema de salas

```text
/general
/linux
/python
```

Cada sala con usuarios independientes.

Ese ejercicio ya te acerca a la arquitectura básica de Discord o IRC.

---

# 17. Reflexión técnica

Los sockets son una de las capas más importantes de la informática moderna.

Cuando entiendes sockets, empiezas a entender:

- internet,
- protocolos,
- servicios distribuidos,
- infraestructura cloud,
- ciberseguridad,
- sistemas operativos.

Muchos programadores usan APIs toda su vida sin comprender realmente qué ocurre debajo.  
Los sockets son una de las puertas de

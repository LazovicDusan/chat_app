import threading
import socket

global stop_thread

host = "127.0.0.1" #localhost
port = 3333

nickname = input("Enter your nickname please: ")
if nickname == "admin":
    password = input("Enter admin password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    stop_thread = False
    while True:
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
                next_message = client.recv(1024).decode("ascii")
                if next_message == "PASSWORD":
                    client.send(password.encode("ascii"))
                    if client.recv(1024).decode("ascii") == "REFUSE":
                        print("Connection has been refused! \nWrong password!")
                        stop_thread = True
                    elif next_message == "BAN":
                        print("Connection refused due to ban!")
                        client.close()
                        stop_thread = True
                else:
                    print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    stop_thread = False
    while True:
        if stop_thread:
            break
        message = f"{nickname}: {input('')}"
        if message[len(nickname)+2:].startswith("/"):
            if nickname == "admin":
                if message[len(nickname)+2:].startswith("/kick"):
                    client.send(f"KICK {message[len(nickname)+8]}".encode("ascii"))
                elif message[len(nickname)+2:].startswith("/ban"):
                    client.send(f"BAN {message[len(nickname)+7]}".encode("ascii"))
                else:
                    client.send(message.encode("ascii"))
            else:
                if message[len(nickname)+2:].startswith("/kick") or message[len(nickname)+2:].startswith("/ban"):
                    print("Commands can only be executed by the admin!")
                else:
                    client.send(message.encode("ascii"))
        else:
            client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


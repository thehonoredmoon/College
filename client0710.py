import socket
import threading

def listen_messages(sock):
    """Поток для приёма сообщений от сервера"""
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))

    # Ввод имени
    name = input("Введите имя: ")
    client.send(f"Имя:{name}".encode("utf-8"))

    # Поток для получения сообщений
    thread = threading.Thread(target=listen_messages, args=(client,))
    thread.start()

    # Отправка сообщений
    while True:
        msg = input()
        if msg == "exit":
            client.send(msg.encode("utf-8"))
            print("Соединение закрыто")
            client.close()
            break
        client.send(msg.encode("utf-8"))


if __name__ == "__main__":
    main()

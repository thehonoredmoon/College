import socket
import threading

clients = {}  # conn -> name

def handle_client(conn, addr):
    name = ""
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break

            # Первое сообщение клиента = его имя
            if msg.startswith("Имя:"):
                name = msg.split(":", 1)[1]
                clients[conn] = name
                print(f"{addr} подключился как {name}")
                continue

            # Команда выхода
            if msg == "exit":
                print(f"{name} покинул чат")
                conn.send("Соединение закрыто".encode("utf-8"))
                break

            # Вывод на сервер
            print(f"{name}: {msg}")

            # Рассылка всем остальным клиентам
            for c in clients:
                if c != conn:
                    c.send(f"{name}: {msg}".encode("utf-8"))

        except:
            break

    if conn in clients:
        del clients[conn]
    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen(5)
    print("Сервер запущен")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()

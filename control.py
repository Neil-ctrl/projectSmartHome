import socket

ESP32_IP = "esp32.local"
PORT = 5000

sock = None


def connect():

    # kept for compatibility with main.py
    # no persistent socket needed anymore

    try:

        ip = socket.gethostbyname(ESP32_IP)

        print(f"Resolved {ESP32_IP} -> {ip}")

        print("ESP32 reachable")

    except Exception as e:

        print("Connection error:", e)


def send_command(command):

    try:

        # resolve hostname every send
        ip = socket.gethostbyname(ESP32_IP)

        print(f"Resolved {ESP32_IP} -> {ip}")

        # fresh socket per command
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect
        sock.connect((ip, PORT))

        # send command
        sock.send((command + "\n").encode())

        print("Sent:", command)

        # close cleanly
        sock.close()

    except Exception as e:

        print("Control error:", e)
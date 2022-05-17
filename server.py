import socket 
import threading

HEADER = 64
PORT = 5555
# we can either manually check the host ip using ifconfig in terminal
# but the better way to call socket.gethostname() function that automatically fetches it for us
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


# SOCK_STREAM is for TCP
# we can change it to SOCK_SEQPACKET for UDP if needed
# socket.AF_INET is telling it that we are using IPV4 address
# similarly we can change it to AF_INET6 for IPV6 addressing
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# handle_client is the main program 
# we are using python socket library that has all the functions required

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.")

    connected = True
    while connected:
        # .recv is the function call that gets the msg from connected client
        msg_length = conn.recv(HEADER).decode('utf-8')
        # if recieved a msg other wise it will go on infinite loop
        if msg_length:
            msg_length = int(msg_length)
            #  decode into utf-8 format to be readble by us
            msg = conn.recv(msg_length).decode('utf-8')

            print(f"{addr} {msg}")
            # calling the reverse fiunction to reverse the message
            conn.send(f"reversed message: {reverse(msg)}".encode(FORMAT))
            
            if msg == "DISCONNECT":
                connected = False
    conn.close()

def reverse(string):
    return string[::-1]

# start is the function for actual call and it is threaded
def start():
    server.listen()
    print(f"LISTENING on {SERVER}...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.activeCount() - 1}")


print("SERVER STARTING")
start()


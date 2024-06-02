from socket import *
import base64

def prompt_for_pop3_credentials():
    pop3_address = input("Enter the POP3 server address (e.g., pop3.mailtrap.io): ")
    pop3_port = int(input("Enter the POP3 server port (e.g., 1100): "))
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return (pop3_address, pop3_port, username, password)

def create_client_socket(mailserver, username, password):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserver)
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    print("Message after connection request:" + recv)
    if recv[:3] != '+OK':
        print('220 reply not received from server.')

    base64_str = ("\x00"+username+"\x00"+password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    clientSocket.send(authMsg)
    recv_auth = clientSocket.recv(1024)
    print(recv_auth.decode())

    return clientSocket

def get_emails():
    pop3_address, pop3_port, username, password = prompt_for_pop3_credentials()
    mailserver = (pop3_address, pop3_port)
    clientSocket = create_client_socket(mailserver, username, password)

    stat = "STAT\r\n"
    clientSocket.send(stat.encode())
    recv_stat = clientSocket.recv(1024)
    print(recv_stat.decode())

    list_cmd = "LIST\r\n"
    clientSocket.send(list_cmd.encode())
    recv_list = clientSocket.recv(1024)
    print(recv_list.decode())

    # Parse the list of emails and their sizes
    emails = []
    lines = recv_list.decode().splitlines()
    for line in lines:
        if "+" in line:
            index = line.split()[1]
            emails.append(index)

    # Download each email
    for email_index in emails:
        retr = f"RETR {email_index}\r\n"
        print(retr)
        clientSocket.send(retr.encode())

        mail = b""
        while True:
            part = clientSocket.recv(1024)
            mail += part
            if part[-5:] == b"\r\n.\r\n":
                break
        
        mail = mail.decode()

        filename = f"email_{email_index}.txt"
        with open(filename, 'a') as file:  # Append mode instead of write mode
            file.write(mail + "\n\n")  # Add newline after each email content

        print(f"Email {email_index} saved to {filename}")

    quit_cmd = "QUIT\r\n"
    clientSocket.send(quit_cmd.encode())
    recv_quit = clientSocket.recv(1024)
    print(recv_quit.decode())
    clientSocket.close()

get_emails()
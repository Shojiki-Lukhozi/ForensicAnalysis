import socket
import base64

def prompt_for_pop3_credentials():
    """Prompt user for POP3 server address, port, username, and password."""
    pop3_address = input("Enter the POP3 server address (e.g., pop3.mailtrap.io): ")
    pop3_port = int(input("Enter the POP3 server port (e.g., 1100): "))
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return pop3_address, pop3_port, username, password

def create_client_socket(mailserver, username, password):
    """Create and return a connected client socket with the mail server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(mailserver)
    
    recv = client_socket.recv(1024).decode()
    print("Message after connection request: " + recv)
    if not recv.startswith('+OK'):
        raise Exception('220 reply not received from server.')
    
    # Encode username and password for authentication
    auth_msg = f'\x00{username}\x00{password}'
    auth_msg = base64.b64encode(auth_msg.encode()).decode()
    client_socket.sendall(f"AUTH PLAIN {auth_msg}\r\n".encode())
    recv_auth = client_socket.recv(1024).decode()
    print(recv_auth)
    
    return client_socket

def get_emails():
    """Fetch emails from the POP3 server and save them to separate files."""
    pop3_address, pop3_port, username, password = prompt_for_pop3_credentials()
    mailserver = (pop3_address, pop3_port)
    
    try:
        client_socket = create_client_socket(mailserver, username, password)
        
        # Retrieve email statistics
        client_socket.sendall(b"STAT\r\n")
        recv_stat = client_socket.recv(1024).decode()
        print(recv_stat)
        
        # Retrieve list of emails
        client_socket.sendall(b"LIST\r\n")
        recv_list = client_socket.recv(1024).decode()
        print(recv_list)
        
        emails = []
        for line in recv_list.splitlines():
            if line.startswith('+OK') or not line.strip():
                continue
            index = line.split()[0]
            emails.append(index)
        
        # Fetch each email and save to a file
        for email_index in emails:
            client_socket.sendall(f"RETR {email_index}\r\n".encode())
            
            mail = b""
            while True:
                part = client_socket.recv(1024)
                mail += part
                if part.endswith(b"\r\n.\r\n"):
                    break
            
            mail = mail.decode('utf-8', errors='ignore')  # Added error handling for decoding
            filename = f"email_{email_index}.txt"
            with open(filename, 'w', encoding='utf-8') as file:  # Explicitly setting encoding
                file.write(mail)
            
            print(f"Email {email_index} saved to {filename}")
        
        # Close connection
        client_socket.sendall(b"QUIT\r\n")
        recv_quit = client_socket.recv(1024).decode()
        print(recv_quit)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

get_emails()

import socket
import base64
from email import parser
from email.header import decode_header
from email.utils import parseaddr

def decode_header_value(value):
    """Decode email header value."""
    decoded_parts = decode_header(value)
    return ''.join([str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else str(part[0]) for part in decoded_parts])

def get_body(msg):
    """Extract and decode the email body."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode('utf-8')
            elif content_type == "text/html" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode('utf-8')
    else:
        return msg.get_payload(decode=True).decode('utf-8')


def create_client_socket(mailserver, username, password):
    """Create and return a connected client socket with the mail server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
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
    pop3_address="pop3.mailtrap.io"
    pop3_port=1100
    username=""
    password =""
    mailserver = (pop3_address, pop3_port)
    
    try:
        client_socket = create_client_socket(mailserver, username, password)
        
        # Retrieve email statistics
        client_socket.sendall(b"STAT\r\n")
        recv_stat = client_socket.recv(1024).decode()
        print(recv_stat)
        
        # Retrieve list of emails
        client_socket.sendall(b"LIST\r\n")
        response = b""
        while True:
            part = client_socket.recv(1024)
            response += part
            if b"\r\n.\r\n" in part:
                break
        
        recv_list = response.decode()

        print(recv_list,'TEST_1')
        
        emails = []
        
        lines = recv_list.splitlines()
        print('TEST_2',lines)
        for line in lines:
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit():
                index = parts[0]
                emails.append(index)
        print(line,'TEST_3')
        # Fetch each email and save to a file
        for email_index in emails:
            print(emails,'TEST_4')
            client_socket.sendall(f"RETR {email_index}\r\n".encode())
            
            mail = b""
            while True:
                part = client_socket.recv(1024)
                print('TEST_HANG')
                
                mail += part
                if part.endswith(b"\r\n.\r\n"):
                    break
            print('TEST_5')
            
            print(mail,'TEST_6') # Added error handling for decoding
            msg = parser.BytesParser().parsebytes(mail)

            subject =parseaddr(msg['Subject'])
            from_ = parseaddr(msg['From'])[1]
            to_ = parseaddr(msg['To'])[1]
            body = get_body(msg)
            print('TEST_7')
            print(f"Email {email_index}:")
            print(f"Subject: {subject}")
            print(f"From: {from_}")
            print(f"To: {to_}")
            print(f"Body:\n{body}\n")

            filename = f"email_{email_index}.txt"
            with open(filename, 'w', encoding='utf-8') as file:  # Explicitly setting encoding
                file.write(f"Subject: {subject}\n")
                file.write(f"Body:\n{body}\n")
            
        print(f"Email {email_index} saved to {filename}")
        
        # Close connection
        client_socket.sendall(b"QUIT\r\n")
        recv_quit = client_socket.recv(1024).decode()
        print(recv_quit)
    
    except socket.timeout:
        print("Connection timed out. Please check your network connection and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

get_emails()

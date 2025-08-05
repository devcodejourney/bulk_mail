import socket
import ssl
import time
import logging
import base64
from config import EMAIL_CONFIG

class EmailSender:
    def __init__(self):
        self.retries = EMAIL_CONFIG['retries']
        self.timeout = EMAIL_CONFIG['timeout']
        self.delay = EMAIL_CONFIG['delay']
    
    def _expect_response(self, sock, expected_code):
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        if not response.startswith(str(expected_code)):
            raise Exception(f"Unexpected SMTP response: {response.strip()}")
        return response
    
    def _smtp_command(self, sock, command, expected_code=250):
        sock.sendall(command.encode() + b"\r\n")
        return self._expect_response(sock, expected_code)
    
    def _starttls(self, sock):
        try:
            # Send STARTTLS command
            self._smtp_command(sock, "STARTTLS", 220)
            
            # Create SSL context
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            
            # Wrap the socket
            return context.wrap_socket(
                sock,
                server_hostname=EMAIL_CONFIG['mta_server']
            )
        except Exception as e:
            raise Exception(f"TLS handshake failed: {str(e)}")
    
    def _authenticate(self, sock):
        try:
            self._smtp_command(sock, "AUTH LOGIN", 334)
            self._smtp_command(sock, base64.b64encode(
                EMAIL_CONFIG['smtp_username'].encode()).decode(), 334)
            self._smtp_command(sock, base64.b64encode(
                EMAIL_CONFIG['smtp_password'].encode()).decode(), 235)
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")
    
    def send(self, email_package):
        for attempt in range(self.retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.timeout)
                    logging.info(f"Connecting to {EMAIL_CONFIG['mta_server']}:{EMAIL_CONFIG['mta_port']}")
                    
                    # Connect to server
                    # ব্যবহার করুন:
                    context = ssl.create_default_context()
                    sock = context.wrap_socket(
                        socket.socket(socket.AF_INET),
                        server_hostname=EMAIL_CONFIG['mta_server']
                    )
                    sock.connect((EMAIL_CONFIG['mta_server'], EMAIL_CONFIG['mta_port']))
                    logging.debug(f"Server welcome: {welcome.strip()}")
                    
                    # Send EHLO
                    ehlo_response = self._smtp_command(sock, 
                        f"EHLO {socket.gethostname()}")
                    logging.debug(f"EHLO response: {ehlo_response.strip()}")
                    
                    # Start TLS
                    sock = self._starttls(sock)
                    logging.info("TLS connection established successfully")
                    
                    # Re-send EHLO after STARTTLS
                    ehlo_response = self._smtp_command(sock, 
                        f"EHLO {socket.gethostname()}")
                    logging.debug(f"EHLO after TLS: {ehlo_response.strip()}")
                    
                    # Authenticate
                    self._authenticate(sock)
                    logging.info("Authenticated successfully")
                    
                    # Send email
                    self._smtp_command(sock, 
                        f"MAIL FROM:<{EMAIL_CONFIG['sender_email']}>")
                    self._smtp_command(sock, 
                        f"RCPT TO:<{email_package['to']}>")
                    self._smtp_command(sock, "DATA", 354)
                    
                    # Send email data
                    sock.sendall(email_package['data'].encode() + b"\r\n.\r\n")
                    self._expect_response(sock, 250)
                    
                    # Quit
                    self._smtp_command(sock, "QUIT", 221)
                    logging.info(f"Email sent successfully to {email_package['to']}")
                    return True
            
            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed: {str(e)}")
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                    continue
                logging.error(f"Failed to send after {self.retries} attempts")
                return False
import logging
import socket
import ssl
import time

from bmailer.utils.decode_config import _decode

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class EmailSender:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        sender_email: str,
        retries: int = 3,
        timeout: int = 30,
        delay: int = 2,
    ) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        self.retries = retries
        self.timeout = timeout
        self.delay = delay

    def _expect_response(self, sock: socket.socket, expected_code: int) -> str:
        response = sock.recv(1024).decode("utf-8", errors="ignore")
        if not response.startswith(str(expected_code)):
            raise Exception(f"Unexpected SMTP response: {response.strip()}")
        return response

    def _smtp_command(
        self,
        sock: socket.socket,
        command: str,
        expected_code: int = 250,
    ) -> str:
        sock.sendall(command.encode() + b"\r\n")
        return self._expect_response(sock, expected_code)

    def _starttls(self, sock: socket.socket):
        try:
            self._smtp_command(sock, "STARTTLS", 220)
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            return context.wrap_socket(sock, server_hostname=self.smtp_server)
        except Exception as e:
            raise Exception(f"TLS handshake failed: {str(e)}")

    def _authenticate(self, sock):
        try:
            self._smtp_command(sock, "AUTH LOGIN", 334)
            self._smtp_command(sock, _decode(self.smtp_username), 334)
            self._smtp_command(sock, _decode(self.smtp_password), 235)
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

    def send(self, email_package):
        for attempt in range(self.retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.timeout)
                    logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}")

                    # For port 465 (SMTPS), use direct SSL connection
                    if self.smtp_port == 465:
                        context = ssl.create_default_context()
                        context.minimum_version = ssl.TLSVersion.TLSv1_2
                        sock = context.wrap_socket(
                            sock, server_hostname=self.smtp_server
                        )

                    sock.connect((self.smtp_server, self.smtp_port))

                    # Read server welcome message
                    welcome = self._expect_response(sock, 220)
                    logger.debug(f"Server welcome: {welcome.strip()}")

                    host_name = socket.gethostname()
                    ehlo_response = self._smtp_command(sock, f"EHLO {host_name}")
                    logger.debug(f"EHLO response: {ehlo_response.strip()}")

                    # For ports 587/25 (SMTP with STARTTLS), upgrade to TLS
                    if self.smtp_port in [587, 25]:
                        sock = self._starttls(sock)
                        logger.info("TLS connection established successfully")

                        # Re-send EHLO after STARTTLS
                        ehlo_response = self._smtp_command(sock, f"EHLO {host_name}")
                        logger.debug(f"EHLO after TLS: {ehlo_response.strip()}")

                    # Authenticate
                    self._authenticate(sock)
                    logger.info("Authenticated successfully")

                    # Send email
                    self._smtp_command(sock, f"MAIL FROM:<{self.sender_email}>")
                    self._smtp_command(sock, f"RCPT TO:<{email_package['to']}>")
                    self._smtp_command(sock, "DATA", 354)

                    # Send email data
                    sock.sendall(email_package["data"].encode() + b"\r\n.\r\n")
                    self._expect_response(sock, 250)

                    # Quit
                    self._smtp_command(sock, "QUIT", 221)
                    logger.info(f"Email sent successfully to {email_package['to']}")
                    return True

            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                    continue
                logger.error(f"Failed to send after {self.retries} attempts")
                return False

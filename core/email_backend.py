import socket
from django.core.mail.backends.smtp import EmailBackend

class IPv4EmailBackend(EmailBackend):
    def open(self):
        # Monkey-patch socket.getaddrinfo to filter out IPv6 for the duration of the connection
        # This is necessary because some environments (like Render) might have issues with IPv6 routing
        # to Gmail, causing "Network is unreachable" errors.
        
        original_getaddrinfo = socket.getaddrinfo

        def ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            # Force AF_INET (IPv4)
            return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

        socket.getaddrinfo = ipv4_getaddrinfo
        try:
            return super().open()
        finally:
            # Restore the original getaddrinfo
            socket.getaddrinfo = original_getaddrinfo

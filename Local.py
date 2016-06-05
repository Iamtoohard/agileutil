import socket

class Local:

    @staticmethod
    def hostname():
        return socket.gethostname()

    @staticmethod
    def ip():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def ipList():
        return socket.gethostbyname_ex(socket.gethostname())


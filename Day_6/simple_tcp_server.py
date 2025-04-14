from socket import socket, AF_INET, SOCK_STREAM, SOMAXCONN, SHUT_RD, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT
import logging
import logging.config

logging.basicConfig(filename="simple_socket_server.log", 
                    level=logging.DEBUG,
                    format="%(asctime)s: %(name)s: %(levelname)s: %(message)s"
)


class TCPServer:
    def __init__(self, hostname, port, handler):
        self.hostname, self.port, self.handler = hostname, port, handler
        self.log = logging.getLogger(self.__class__.__name__)
        self.quit = False

    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

        self.log.debug(f"Binding socket to {self.hostname}:{self.port}")
        self.sock.bind((self.hostname, self.port))
        self.log.debug("Setting up the listen queue...")
        self.sock.listen(SOMAXCONN)

    def shutdown(self):
         self.sock.shutdown(SHUT_RD)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, et, ev, tb):
        self.shutdown()
        self.quit = True

    def serve_forever(self):
        while not self.quit:
            self.log.info("Waiting for incoming connection...")
            client, addrinfo = self.sock.accept()
            self.log.debug(f"Got incoming connection from {addrinfo}")
            self.handler(client, addrinfo)
            client.close()



class EchoHandler:
    def __init__(self, conn, addrinfo):
        self.conn, self.addrinfo = conn, addrinfo
        
        self.ins, self.outs = conn.makefile("r"), conn.makefile("w")
        self.log = logging.getLogger(self.__class__.__name__)
        
        self.run()
        
        self.ins.close()
        self.outs.close()

    def run(self):
            while True:
                self.log.debug(f"Waiting for client message from {self.addrinfo}")
                line = self.ins.readline()
                self.log.debug(f"Got message from {self.addrinfo}: {line.strip()}")

                if "exit" in line:
                    self.log.debug(f"Got an 'exit' message from {self.addrinfo}") 
                    break
                self.outs.write(line.upper())
                self.outs.flush()



if __name__ == '__main__':
    try:
        with TCPServer(hostname="localhost", port=9876, handler=EchoHandler) as server:
            server.serve_forever()
    finally:
        print("Exiting...")
        
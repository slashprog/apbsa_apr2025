#from gevent import monkey; monkey.patch_all()

from threading import Thread, current_thread as current
from concurrent.futures import ThreadPoolExecutor as Executor

from socket import socket, AF_INET, SOCK_STREAM, SOMAXCONN, SHUT_RD, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT
import logging
import logging.config

logging.basicConfig(filename="simple_socket_server.log", 
                    level=logging.DEBUG,
                    format="%(asctime)s: %(name)s: %(levelname)s: %(message)s"
)


class TCPServer:
    def __init__(self, hostname, port, handler, max_connections=10):
        self.hostname, self.port, self.handler = hostname, port, handler
        self.max_connections = max_connections
        self.log = logging.getLogger(self.__class__.__name__)
        self.quit = False
        self.clients = []

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
        with Executor(max_workers=self.max_connections) as workers:
            while not self.quit:
                self.log.info("Waiting for incoming connection...")
                client, addrinfo = self.sock.accept()
                self.log.debug(f"Got incoming connection from {addrinfo}")
                client_handler = workers.submit(self.handler, client, addrinfo)
                self.clients.append(client_handler)
                #Thread(target=self.handler, args=(client, addrinfo)).start() 
                #self.handler(client, addrinfo)

class EchoHandler:
    def __init__(self, conn, addrinfo):
        self.log = logging.getLogger(self.__class__.__name__)
        self.conn, self.addrinfo = conn, addrinfo
        self.ins, self.outs = conn.makefile("r"), conn.makefile("w")
        self.log.debug(f"Running EchoHandler as {current().name}")        
        self.run()
        
        self.ins.close()
        self.outs.close()
        self.conn.close()

    def run(self):
            while True:
                self.log.debug(f"{current().name}: Waiting for client message from {self.addrinfo}")
                line = self.ins.readline()
                self.log.debug(f"{current().name}: Got message from {self.addrinfo}: {line.strip()}")

                if "exit" in line:
                    self.log.debug(f"{current().name}: Got an 'exit' message from {self.addrinfo}") 
                    break
                self.outs.write(line.upper())
                self.outs.flush()
            self.log.debug(f"{current().name}: exiting run() loop")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("hostname")
    parser.add_argument("--port", type=int, default=9876)
    args = parser.parse_args()

    try:
        with TCPServer(hostname=args.hostname, port=args.port, handler=EchoHandler) as server:
            server.serve_forever()
    finally:
        print("Exiting...")

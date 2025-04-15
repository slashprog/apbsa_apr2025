#from gevent import monkey; monkey.patch_all()

from threading import Thread, current_thread as current
from concurrent.futures import ThreadPoolExecutor as Executor

from socket import socket, AF_INET, SOCK_STREAM, SOMAXCONN, SHUT_RD, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT
import logging
import logging.config

logging.basicConfig(filename="/tmp/fileserver/simple_file_server.log", 
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

class FileServer:
    def __init__(self, conn, addrinfo):
        self.log = logging.getLogger(self.__class__.__name__)
        self.conn, self.addrinfo = conn, addrinfo
        self.ins, self.outs = conn.makefile("r"), conn.makefile("w")
        self.quit = False
        self.path = "/tmp/fileserver/files"
        self.log.debug(f"Running FileServer as {current().name}")
        self.log.debug(f"Serving files from {self.path}")       
        self.run()
        
        self.ins.close()
        self.outs.close()
        self.conn.close()

    def run(self):
            while not self.quit:
                self.log.debug(f"{current().name}: Waiting for client message from {self.addrinfo}")
                line = self.ins.readline().strip()
                self.log.debug(f"{current().name}: Got message from {self.addrinfo}: {line}")

                command, *args = line.split()

                if hasattr(self, command):
                    cmd = getattr(self, command)
                    cmd(*args)
                else:
                    print("400 INVALID_COMMAND", file=self.outs, flush=True)

            self.log.debug(f"{current().name}: exiting run() loop")

    def get(self, filename):
        self.log.info(f"{current().name}:{self.addrinfo}: get request for file {filename}")
        print("200 OK", file=self.outs, flush=True)

    def put(self, filename):
        self.log.info(f"{current().name}:{self.addrinfo}: put request for file {filename}")
        print("201 CREATED", file=self.outs, flush=True)

    def list(self):
        self.log.info(f"{current().name}:{self.addrinfo}: listing files")
        print("220 LISTING", file=self.outs, flush=True)

    def exit(self):
        self.log.info(f"{current().name}:{self.addrinfo}: closing connection")
        print("330 BYE", file=self.outs, flush=True)
        self.quit = True


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("hostname")
    parser.add_argument("--port", type=int, default=9876)
    args = parser.parse_args()

    with TCPServer(hostname=args.hostname, port=args.port, handler=FileServer) as server:
        server.serve_forever()

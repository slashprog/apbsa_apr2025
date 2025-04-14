

class TCPServer:
    def __init__(self, hostname, port, handler):
        pass # TODO

    # ...


class EchoHandler:
    def __init__(self, conn, addrinfo):
        self.conn, self.addrinfo = conn, addrinfo

    def run(self):
            while True:
                line = self.ins.readline()
                self.log.debug(f"Got message from {addrinfo}: {line.strip()}")

                if "exit" in line:
                    self.log.debug(f"Got an 'exit' message from {addrinfo}") 
                    break
                self.outs.write(line.upper())
                self.outs.flush()

    # ...

if __name__ == '__main__':

    server = TCPServer(hostname="localhost", port=9876, handler=EchoHandler)
    server.serve_forever()
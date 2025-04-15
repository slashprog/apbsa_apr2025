from socket import socket, AF_INET, SOCK_STREAM

class FileClient:
    def __init__(self, conn, addrinfo):
        self.conn, self.addrinfo = conn, addrinfo
        self.ins, self.outs = self.conn.makefile("r"), self.conn.makefile("w")
        self.quit = False

        self.run()

        self.ins.close()
        self.outs.close()

    def run(self):
        while not self.quit:
            command = input("FileClient> ")
            print(command, file=self.outs, flush=True)
            reply = self.ins.readline()

            print(reply)
            if "BYE" in reply:
                self.quit = True


    def exit(self):
        self.quit = True

    def get(self, filename):
        print(f"get {filename}", file=self.outs, flush=True)
        reply = self.ins.readline()

    def put(self, filename):
        print(f"put {filename}", file=self.outs, flush=True)
        reply = self.ins.readline()

    def list(self):
        print("list", file=self.outs, flush=True)
        reply = self.ins.readline()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("hostname")
    parser.add_argument("--port", type=int, default=9876)
    args = parser.parse_args()

    print(f"Creating connection to {args.hostname}:{args.port}")
    try:
        conn = socket(AF_INET, SOCK_STREAM)
        conn.connect((args.hostname, args.port))
        
        FileClient(conn, (args.hostname, args.port))

    finally:
        conn.close()


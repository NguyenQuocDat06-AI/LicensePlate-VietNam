from http.server import HTTPServer
import server

HOST = '0.0.0.0'
PORT = 9049

if __name__ == "__main__":
    server.start(HOST, PORT)

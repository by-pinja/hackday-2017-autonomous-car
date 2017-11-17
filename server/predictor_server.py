import io
import socket
import sys
from learning.predictor import Predictor


class PredictorServer(object):
    """
    Server which takes input images from RC car and provides steering data from ML model
    """
    HOST = ''   # all available interfaces
    PORT = 8888  # non-privileged port
    MODEL_DIR = r"E:\test_model"

    def __init__(self, port=None, modelpath=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port is not None:
            self.PORT = port
        if modelpath is not None:
            self.MODEL_DIR = modelpath
        try:
            self.socket.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Start listening on socket
        self.socket.listen(10)
        print('Socket now listening')

        self.predictor = Predictor(self.MODEL_DIR)

        conn, addr = self.socket.accept()
        print('Connected from ' + addr[0] + ':' + str(addr[1]))
        while True:
            content = io.BytesIO()
            while True:
                part = conn.recv(1024)
                if part.endswith('EOM'.encode('UTF-8')):
                    content.write(part[:-3])
                    break
                content.write(part)

            bytes = content.getvalue()
            print("Received content")
            result = self.predictor.read(bytes)
            print(result)
            conn.sendall("{},{}".format(result['result'][0][0], result['result'][0][1]).encode('UTF-8'))

        self.socket.close()


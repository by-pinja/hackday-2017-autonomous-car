import socket
import sys
import io

from camera import CameraModule
from piggy import Piggy


class AiClient:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = int(port)
        print("ip: %s, port: %s" % (self.ip, self.port))

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.camera_module = CameraModule()
        self.piggy = Piggy()
        self.piggy.initPiggy()

        # Connect the socket to the port where the server is listening
        server_address = (self.ip, self.port)
        print('+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+')
        print('connecting to address %s at port %s' % server_address)
        print('+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+|+')
        self.sock.connect(server_address)
        self.start_loop()

    def start_loop(self):

       while(True):
           image_data = self.camera_module.capture_image_string()
           response = self.request_data(image_data)
           self.steer_piggy(response)

    def steer_piggy(self, instruction):
        if instruction:
            # Steer the car
            if instruction[0] < 0:
                self.piggy.turnCarLeft(255)
            else:
                self.piggy.turnCarRight(255)
            # Control acceleration
            self.piggy.accelerateCar(int(-(instruction[1])*255))

    def request_data(self, message):

        print('sending "%s"' % message)
        self.sock.sendall(message)
        self.sock.sendall("EOM")
        print('all sent')
        response = self.sock.recv(4096)
        print(response)
        if "," in response:
            steering, propagation = response.split(",")
            return steering, propagation
        else:
            print("Could not process response %" % response)
            return None

if __name__=='__main__':
    AiClient(sys.argv[1], sys.argv[2])


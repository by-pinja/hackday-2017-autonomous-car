import pigpio
import datetime
import time
#usage:
#create Piggy object: piggy = Piggy()
#initialize: piggy.initPiggy()
#accelerateCar, reverseCar, turnCarLeft, turnCarRight: strength = 0...255
#stopCar, no args
#disconnect: piggy.disconnect()

class Pin:
    FORWARD = 2
    REVERSE = 3
    LEFT = 4
    RIGHT = 14

class Piggy:
    def __init__(self):
        print("Piggy::__init__")

    #set_PWM_dutycycle(user_gpio, dutycycle=0...255)
    def stopCar(self):
        print(datetime.datetime.now(), ": stopCar")
        self.p.set_PWM_dutycycle(Pin.FORWARD, 0)
        self.p.set_PWM_dutycycle(Pin.REVERSE, 0)
        self.p.set_PWM_dutycycle(Pin.LEFT, 0)
        self.p.set_PWM_dutycycle(Pin.RIGHT, 0)

    def accelerateCar(self, strength):
        print(datetime.datetime.now(), ": accelerateCar: ", strength)
        self.p.set_PWM_dutycycle(Pin.REVERSE, 0)
        self.p.set_PWM_dutycycle(Pin.FORWARD, strength)

    def reverseCar(self, strength):
        print(datetime.datetime.now(), ": reverseCar: ", strength)
        self.p.set_PWM_dutycycle(Pin.FORWARD, 0)
        self.p.set_PWM_dutycycle(Pin.REVERSE, strength)

    def turnCarLeft(self, strength):
        print(datetime.datetime.now(), ": turnCarLeft: ", strength)
        self.p.set_PWM_dutycycle(Pin.RIGHT, 0)
        self.p.set_PWM_dutycycle(Pin.LEFT, round(strength))

    def turnCarRight(self, strength):
        print(datetime.datetime.now(), ": turnCarRight: ", strength)
        self.p.set_PWM_dutycycle(Pin.LEFT, 0)
        self.p.set_PWM_dutycycle(Pin.RIGHT, round(strength))

    def disconnect(self):
        print(datetime.datetime.now(), ": disconnect")
        self.p.stop()

    def setupPwmFrequency(self, pwm_frequency_hz):
        print(datetime.datetime.now(), ": setupPwmFrequency: ", pwm_frequency_hz)
        #sample rate default on 5 microseconds
        #set_PWM_frequency(user_gpio, frequency)
        self.p.set_PWM_frequency(Pin.FORWARD, pwm_frequency_hz)
        self.p.set_PWM_frequency(Pin.REVERSE, pwm_frequency_hz)
        self.p.set_PWM_frequency(Pin.LEFT, pwm_frequency_hz)
        self.p.set_PWM_frequency(Pin.RIGHT, pwm_frequency_hz)

    def initPiggy(self):
        print(datetime.datetime.now(), ": initPiggy...")
        #self.p = pigpio.pi("192.168.100.23", 8888)
        self.p = pigpio.pi()
        if not self.p.connected:
            print("UNABLE TO CONNECT TO PIGPIO DAEMON")
            exit()
        print(datetime.datetime.now(), ": Setting mode...")
        self.p.set_mode(Pin.FORWARD, pigpio.OUTPUT)
        self.p.set_mode(Pin.REVERSE, pigpio.OUTPUT)
        self.p.set_mode(Pin.LEFT, pigpio.OUTPUT)
        self.p.set_mode(Pin.RIGHT, pigpio.OUTPUT)
        print(datetime.datetime.now(), ": clearing pins 0-31...")
        for pin in range(0,31):
            self.p.write(pin, 0)
        print(datetime.datetime.now(), ": setting up PWM frequency...")
        self.setupPwmFrequency(100)
    
    def runTest(self):
        waitSeconds = 10
        self.initPiggy()
        print(datetime.datetime.now(), ": running test...")
        self.accelerateCar(255);
        time.sleep(waitSeconds)
        self.stopCar()
        #self.reverseCar(255);
        #self.turnCarLeft(255);
        #self.turnCarRight(255);
        self.disconnect()
        exit()


class startClass:
    print("running...")
#    piggy = Piggy()
#    piggy.runTest()
#    print("done!")
      

import pigpio
import datetime
import time

class Pin:
    FORWARD = 2
    REVERSE = 3
    LEFT = 4
    RIGHT = 14

class FakePi:
    def pi(self):
        print "FakePi::pi()"
        return self

    def __init__(self):
        self.connected = True
        print datetime.datetime.now(), ": FakePi:__init__"
    
    def set_PWM_dutycycle(self, user_gpio, dutycycle):
        print datetime.datetime.now(), ": set_PWM_dutycycle: user_gpio=", user_gpio,", dutycycle=", dutycycle
        
    def set_PWM_frequency(self, user_gpio, frequency):
        print datetime.datetime.now(), ": set_PWM_frequency: user_gpio=", user_gpio,", frequency=", frequency
        
    def set_mode(self, user_gpio, mode):
        print datetime.datetime.now(), ": set_mode: user_gpio=", user_gpio,", mode=", mode

class Piggy:

    def __init__(self):
        print "ok"

    #set_PWM_dutycycle(user_gpio, dutycycle=0...255)
    def stopCar(self, p):
        print "stopCar"
        p.set_PWM_dutycycle(Pin.FORWARD, 0)
        p.set_PWM_dutycycle(Pin.REVERSE, 0)
        p.set_PWM_dutycycle(Pin.LEFT, 0)
        p.set_PWM_dutycycle(Pin.RIGHT, 0)

    def accelerateCar(self, p, strength):
        print "accelerateCar: ", strength
        p.set_PWM_dutycycle(Pin.REVERSE, 0)
        p.set_PWM_dutycycle(Pin.FORWARD, strength)

    def reverseCar(self, p, strength):
        print "reverseCar: ", strength
        p.set_PWM_dutycycle(Pin.FORWARD, 0)
        p.set_PWM_dutycycle(Pin.REVERSE, strength)

    def turnCarLeft(self, p, strength):
        print "turnCarLeft: ", strength
        p.set_PWM_dutycycle(Pin.RIGHT, 0)
        p.set_PWM_dutycycle(Pin.LEFT, strength)

    def turnCarLeft(self, p, strength):
        print "turnCarRight: ", strength
        p.set_PWM_dutycycle(Pin.RIGHT, 0)
        p.set_PWM_dutycycle(Pin.LEFT, strength)

    def setupPwmFrequency(self, p, pwm_frequency_hz):
        print "setupPwmFrequency: ", pwm_frequency_hz
        #sample rate default on 5 microseconds
        #set_PWM_frequency(user_gpio, frequency)
        p.set_PWM_frequency(Pin.FORWARD, pwm_frequency_hz)
        p.set_PWM_frequency(Pin.REVERSE, pwm_frequency_hz)
        p.set_PWM_frequency(Pin.LEFT, pwm_frequency_hz)
        p.set_PWM_frequency(Pin.RIGHT, pwm_frequency_hz)

    def realInitPiggy(self):
        p = pigpio.pi("192.168.100.23", 8888)
        if not p.connected:
            print "UNABLE TO CONNECT TO PIGPIO DAEMON"
            exit()
        print datetime.datetime.now(), ": Setting mode..."
        p.set_mode(Pin.FORWARD, pigpio.OUTPUT)
        p.set_mode(Pin.REVERSE, pigpio.OUTPUT)
        p.set_mode(Pin.LEFT, pigpio.OUTPUT)
        p.set_mode(Pin.RIGHT, pigpio.OUTPUT)
        print datetime.datetime.now(), ": clearing pins 0-31..."
        for pin in range(0,31):
            p.write(pin, 0)
        print datetime.datetime.now(), ": setting up PWM frequency..."
        self.setupPwmFrequency(p, 100)
        return p

    def fakeInitPiggy(self):
        p = FakePi.pi(FakePi()) #pigpio.pi()
        if not p.connected:
            print "UNABLE TO CONNECT TO PIGPIO DAEMON"
            exit()
        print datetime.datetime.now(), ": Setting mode..."
        p.set_mode(Pin.FORWARD, pigpio.OUTPUT)
        p.set_mode(Pin.REVERSE, pigpio.OUTPUT)
        p.set_mode(Pin.LEFT, pigpio.OUTPUT)
        p.set_mode(Pin.RIGHT, pigpio.OUTPUT)
        self.setupPwmFrequency(p, 100)
        return p
    
    def runRealTest(self):
        waitSeconds = 15
        p = self.realInitPiggy()
        print "running test..."
        self.accelerateCar(p, 255);
        time.sleep(waitSeconds)
        self.stopCar(p)
        #time.sleep(waitSeconds)
        #self.reverseCar(p, 255);
        #time.sleep(waitSeconds)
        #self.stopCar(p);
        #self.turnCarLeft(p, 255);
        #time.sleep(waitSeconds)
        #self.turnCarRight(p, 255);
        #time.sleep(waitSeconds)
        #self.stopCar(p);
        exit()
        
    def runFakeTest(self):
        p = self.fakeInitPiggy()
        self.accelerateCar(p, 255);
        time.sleep(1)
        self.stopCar(p)
        time.sleep(1)
        self.reverseCar(p, 255);
        time.sleep(1)
        self.stopCar(p);
        exit()

class startClass:
    print "running..."
    piggy = Piggy()
    piggy.runRealTest()
    #piggy.runFakeTest()
    print "done!"
      

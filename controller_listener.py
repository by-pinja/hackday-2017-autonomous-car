import pygame
from sampler import Sampler
from piggy import Piggy
pygame.init()

pygame.display.set_caption("PS4 controller listener")


class ControlListener:
    def __init__(self):
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Limit to 10 frames per second
        clock.tick(10)

        # Initialize the joysticks
        pygame.joystick.init()
        self.run_in_progress = False
        self.done = False
        self.sampler = Sampler()
        self.piggy = Piggy()
        self.piggy.initPiggy()

        self.sampling = False
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        self.steering = 0
        self.propagation = 0

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
        
        # Set event types that can enter the queue
        pygame.set_allowed(None)
        pygame.event.set_allowed(
            [pygame.JOYAXISMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]
        )

        self.listen()
        self.piggy.disconnect()

    def listen(self):
        # loops all program lifecycle
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():  # User did something
                if event is None:
                    continue
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop

                # Analog stick events
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 5:
                        self.analog_y_value_change(event.value)
                    elif event.axis == 0:
                        self.analog_x_value_change(event.value)
                # Direction pad events
                elif event.type == pygame.JOYHATMOTION:
                    value = event.value
                    if value == (0, 0):
                        self.go_straight()
                    elif value == (-1, 0):
                        self.turn_left()
                    elif value == (1, 0):
                        self.turn_right()
                elif event.type == pygame.JOYBUTTONDOWN:
                    value = event.button
                    # Action button events
                    if value == 1:
                        self.throttle()
                    elif value == 2:
                        self.reverse()
                    # Start / stop events
                    elif value == 9:
                        if not self.run_in_progress:
                            self.run_in_progress = True
                            self.start_run()
                        elif self.run_in_progress:
                            self.run_in_progress = False
                            self.save_run()
                    elif value == 8:
                        if self.run_in_progress:
                            self.run_in_progress = False
                            self.discard_run()
                elif event.type == pygame.JOYBUTTONUP:
                    value = event.button
                    if value == 1:
                        self.release_throttle()
                    elif value == 2:
                        self.release_reverse()                
                    print(str(event))

    # Start/save/discard a run
    def start_run(self):
        self.sampling = True
        self.sampler.start()

    def save_run(self):
        self.sampler.save_run()
        self.sampling = False

    def discard_run(self):
        print("Discarding the run")
        self.sampling = False
        self.sampler.reject()

    def capture(self):
        if self.sampling:
            self.sampler.capture(self.steering, self.propagation)

    # Directions (left, straight, right)
    def turn_left(self):
        self.steering = -1
        self.piggy.turnCarLeft(255)
        self.capture()

    def turn_right(self):
        self.steering = 1
        self.piggy.turnCarRight(255)
        self.capture()

    def go_straight(self):
        self.steering = 0
        self.piggy.turnCarLeft(0)
        self.capture()
        print("suoraan")

    # Binary value (forward, backwards, idle)
    def throttle(self):
        self.propagation = 1
        self.piggy.accelerateCar(255)
        self.capture()
        print("kaasu")

    def release_throttle(self):
        self.propagation = 0
        self.piggy.accelerateCar(0)
        self.capture()
        print("kaasu pois")

    def reverse(self):
        self.propagation = -1
        self.piggy.reverseCar(255)
        self.capture()
        print("peruutetaan")

    def release_reverse(self):
        self.propagation = 0
        self.piggy.reverseCar(0)
        self.capture()
        print("peruutus pois")

    # Y axis analog value (1...-1). Negative=forward, positive=backwards
    def analog_y_value_change(self, value):
        # Filter the low end of singal
        if value > 0.05 or value < -0.05:
            self.propagation = value
        else:
            self.propagation = 0
        if self.propagation < 0:
            self.piggy.accelerateCar(int(-(self.propagation)*255))
        else:
            self.piggy.reverseCar(int(self.propagation*255))
        self.capture()

    # X axis analog value (1...-1). Positive=right, negative=left
    def analog_x_value_change(self, value):
        # Filter the low end of singal
        if value > 0.05 or value < -0.05:
            self.steering = value
        else:
            self.steering = 0
        if self.steering >= 0:
            self.piggy.turnCarRight(int(self.steering*255))
        else:
            self.piggy.turnCarLeft(int(-(self.steering)*255))
        self.capture()
# init
listener = ControlListener()

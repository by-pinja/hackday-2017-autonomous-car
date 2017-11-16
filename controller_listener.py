import pygame
from .sampler import Sampler
pygame.init()

pygame.display.set_caption("PS4 controller listener")


class ControlListener():
    def __init__(self):
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Limit to 20 frames per second
        clock.tick(20)

        # Initialize the joysticks
        pygame.joystick.init()
        run_in_progress = False
        self.done = False
        self.sampler = Sampler()

        self.sampling = False
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        self.steering = 0
        self.propagation = 0

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

    def listen(self):
        # loops all program lifecycle
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop

                # Analog stick events
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 5:
                        self.analog_y_value_change(event.value)
                    elif event.axis == 0:
                        self.analog_x_value_change(event.value)
                # Direction pad events
                if event.type == pygame.JOYHATMOTION:
                    value = event.value
                    if value == (0, 0):
                        self.go_straight()
                    elif value == (-1, 0):
                        self.turn_left()
                    elif value == (1, 0):
                        self.turn_right()
                if event.type == pygame.JOYBUTTONDOWN:
                    value = event.button
                    # Action button events
                    if value == 1:
                        self.throttle()
                    elif value == 2:
                        self.reverse()
                    # Start / stop events
                    elif value == 9:
                        if not run_in_progress:
                            run_in_progress = True
                            self.start_run()
                        elif run_in_progress:
                            run_in_progress = False
                            self.save_run()
                    elif value == 8:
                        if run_in_progress:
                            run_in_progress = False
                            self.discard_run()
                if event.type == pygame.JOYBUTTONUP:
                    value = event.button
                    if value == 1:
                        self.release_throttle()
                    elif value == 2:
                        self.release_reverse()
                if self.sampling:
                    self.capture()

    # Start/save/discard a run
    def start_run(self):
        self.sampling = True
        self.sampler.start()

    def save_run(self):
        print("Saving the run")
        self.sampling = False

    def discard_run(self):
        print("Discarding the run")
        self.sampling = False
        self.sampler.reject()

    def capture(self):
        self.sampler.capture(self.steering, self.propagation)

    # Directions (left, straight, right)
    def turn_left(self):
        self.steering = -1

    def turn_right(self):
        self.steering = 1

    def go_straight(self):
        self.steering = 0
        print("suoraan")

    # Binary value (forward, backwards, idle)
    def throttle(self):
        self.propagation = 1
        print("kaasu")

    def release_throttle(self):
        self.propagation = 0
        print("kaasu pois")

    def reverse(self):
        self.propagation = -1
        print("peruutetaan")

    def release_reverse(self):
        self.propagation = 0
        print("peruutus pois")

    # Y axis analog value (1...-1). Negative=forward, positive=backwards
    def analog_y_value_change(self, value):
        # Filter the low end of singal
        if value > 0.05 or value < -0.05:
            self.propagation = value
        else:
            self.propagation = 0

    # X axis analog value (1...-1). Positive=right, negative=left
    def analog_x_value_change(self, value):
        # Filter the low end of singal
        if value > 0.05 or value < -0.05:
            self.steering = value
        else:
            self.steering = 0

# init
listener = ControlListener()
import pygame    

pygame.init()

pygame.display.set_caption("PS4 controller listener")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

run_in_progress = False

# Start/save/discard a run
def start_run():
    print("Start")

def save_run():
    print("Saving the run")

def discard_run():
    print("Discarding the run")

# Directions (left, straight, right)
def turn_left():
    print("vasen")

def turn_right():
    print("oikea")

def go_straight():
    print("suoraan")

# Binary value (forward, backwards, idle)
def throttle():
    print("kaasu")

def release_throttle():
    print("kaasu pois")

def reverse():
    print("peruutetaan")

def release_reverse():
    print("peruutus pois")

# Y axis analog value (1...-1). Negative=forward, positive=backwards
def analog_y_value_change(value):
    # Filter the low end of singal
    if value > 0.05 or value < -0.05:
        print(value)    
    
# X axis analog value (1...-1). Positive=right, negative=left
def analog_x_value_change(value):
    # Filter the low end of singal
    if value > 0.05 or value < -0.05:
        print(value)        

while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop       
	
        # Analog stick events
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 5:
                analog_y_value_change(event.value)
            elif event.axis == 0:
                analog_x_value_change(event.value)
        # Direction pad events
        if event.type == pygame.JOYHATMOTION:
            value = event.value
            if value == (0, 0):
                go_straight()
            elif value == (-1, 0):
                turn_left()
            elif value == (1, 0):
                turn_right()
        if event.type == pygame.JOYBUTTONDOWN:
            value = event.button
            # Action button events
            if value == 1:
                throttle()
            elif value == 2:
                reverse()
            # Start / stop events
            elif value == 9:
                if not run_in_progress:
                    run_in_progress = True
                    start_run()
                elif run_in_progress:
                    run_in_progress = False
                    save_run()
            elif value == 8:
                if run_in_progress:
                    run_in_progress = False
                    discard_run()
        if event.type == pygame.JOYBUTTONUP:
            value = event.button
            if value == 1:
                release_throttle()
            elif value == 2:
                release_reverse()
            
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()


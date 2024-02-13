import pygame
import random as rand
import math
import hyperparameter as hp

# ************************************************** GLOBAL INITIALIZATIONS ******************************************
# Initialize pygame variables
pygame.init()
window = pygame.display.set_mode((hp.WIDTH, hp.HEIGHT))

# player ball index (selected ball)
selected_ball_index = None

# list of balls currently on the screen
balls = []

# Game loop setup
running = True
clock = pygame.time.Clock()
# ********************************************************************************************************************

# ************************************************** BALL FUNCTIONS **************************************************
"""
Ball Format:
ball['position'] = [x, y]
ball['velocity'] = [dx, dy]
ball['color'] = (r, g, b)
"""

"""
Called when the user clicks on the screen.
Adds a ball to the screen at the position of the click.

Parameters:
- position: The position of the click on the screen.
"""
def add_ball(clickPosition):
    newBall = {
        'position': list(clickPosition),
        'velocity': [rand.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY), rand.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY)],
        'color': (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))
    }
    balls.append(newBall)

    
"""
Checks if the click is on a ball.

Parameters:
- clickPosition: The position of the click on the screen.
"""
def is_click_on_ball(clickPosition):
    for ball in balls:
        ballDistanceFromClick = get_distance_click_ball(clickPosition, ball)
        
        if ballDistanceFromClick < hp.BALL_RADIUS:
            return True
    return False

"""
Moves the selected ball in the inputted direction.

Parameters:
- dx: The change in the x direction.
- dy: The change in the y direction.
"""
def move_selected_ball(dx, dy):
    if selected_ball_index is not None:
        # screen boundaries conditions
        ballXPos = balls[selected_ball_index]['position'][0]
        ballYPos = balls[selected_ball_index]['position'][1]
        if ballXPos + dx < hp.BALL_RADIUS or \
            ballXPos + dx > hp.WIDTH - hp.BALL_RADIUS:
            dx = 0
        if ballYPos + dy < hp.BALL_RADIUS or \
            ballYPos + dy > hp.HEIGHT - hp.BALL_RADIUS:
            dy = 0
    
        # move the ball
        balls[selected_ball_index]['position'][0] += dx
        balls[selected_ball_index]['position'][1] += dy

"""
Deletes the selected ball.
"""
def delete_selected_ball():
    if selected_ball_index is not None:
        del balls[selected_ball_index]
        selected_ball_index = None

"""
Selects the ball if the click is on a ball.

Parameters:
- click_pos: The position of the click on the screen.
"""
def select_ball(click_pos):
    global selected_ball_index
    for i, ball in enumerate(balls):
        distance = get_distance_click_ball(click_pos, ball)
        if distance < hp.BALL_RADIUS:
            selected_ball_index = i

            # stop the ball from moving so the user knows they have selected it
            balls[selected_ball_index]['velocity'] = [0, 0]
            break

"""
Moves the ball given its velocity and position.

Parameters:
- ball: The ball to move.
"""

def move_ball(ball):    
    ball['position'][0] += ball['velocity'][0]
    ball['position'][1] += ball['velocity'][1]

    # Check boundary conditions: If true, Bounce off walls
    if ball['position'][0] <= hp.BALL_RADIUS or ball['position'][0] >= hp.WIDTH - hp.BALL_RADIUS:
        ball['velocity'][0] *= -1
    if ball['position'][1] <= hp.BALL_RADIUS or ball['position'][1] >= hp.HEIGHT - hp.BALL_RADIUS:
        ball['velocity'][1] *= -1

"""
Bounces balls off each other.

Parameters:
- ball1: The first ball.
- ball2: The second ball.
"""
def bounce_balls(ball1, ball2):
    dx = ball1['position'][0] - ball2['position'][0]
    dy = ball1['position'][1] - ball2['position'][1]
    distance = math.sqrt(dx**2 + dy**2)

    # Check if balls are overlapping
    if distance < 2*hp.BALL_RADIUS:
        # Calculate new velocities
        nx = dx / distance
        ny = dy / distance
        relativeVelocity = 2 * (ball1['velocity'][0] * nx + ball1['velocity'][1] * ny - ball2['velocity'][0] * nx - ball2['velocity'][1] * ny) / 2

        ball1['velocity'][0] -= relativeVelocity * nx
        ball1['velocity'][1] -= relativeVelocity * ny
        ball2['velocity'][0] += relativeVelocity * nx
        ball2['velocity'][1] += relativeVelocity * ny

        # Adjust the position of the balls so they don't overlap
        overlap = 2 * hp.BALL_RADIUS - distance
        correction_factor = overlap / distance / 2  # Divide the overlap distance between the two balls
        ball1['position'][0] += correction_factor * dx
        ball1['position'][1] += correction_factor * dy
        ball2['position'][0] -= correction_factor * dx
        ball2['position'][1] -= correction_factor * dy

"""
Draws the ball onto the window.

Parameters:
- ball: The ball to draw.
"""
def draw_ball(ball):
    pygame.draw.circle(window, ball['color'], (int(ball['position'][0]), int(ball['position'][1])), hp.BALL_RADIUS)

"""
Returns the distance between the click and the ball.

Parameters:
- click_pos: The position of the click on the screen.
- ball: The ball to check the distance from.
"""
def get_distance_click_ball(click_pos, ball):
    return math.sqrt((ball['position'][0] - click_pos[0]) ** 2 + (ball['position'][1] - click_pos[1]) ** 2)
    
# ********************************************************************************************************************

# ************************************************** MAIN FUNCTION **************************************************
def main():
    global running, selected_ball_index, balls

    # Initialize balls given the initial settings
    for _ in range(hp.START_NUM_BALLS):
        add_ball([rand.randint(hp.BALL_RADIUS, hp.WIDTH - hp.BALL_RADIUS), rand.randint(hp.BALL_RADIUS, hp.HEIGHT - hp.BALL_RADIUS)])
        

    while running:
        window.fill(hp.BACKGROUND_COLOR)

        # input handling
        for event in pygame.event.get():
            # if the user closes the window, exit the game
            if event.type == pygame.QUIT:
                running = False

            # if the user clicks on the screen, add a ball if the click is not on a ball
            # otherwise, select the ball that was clicked on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not is_click_on_ball(event.pos):
                    add_ball(event.pos)
                else:
                    select_ball(event.pos)
            
            # if the user presses the delete key, delete the selected ball
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    delete_selected_ball()

        # define the movement of the selected ball based on the user's input through the arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_selected_ball(-hp.DEFAULT_MOVEMENT, 0)
        if keys[pygame.K_RIGHT]:
            move_selected_ball(hp.DEFAULT_MOVEMENT, 0)
        if keys[pygame.K_UP]:
            move_selected_ball(0, -hp.DEFAULT_MOVEMENT,)
        if keys[pygame.K_DOWN]:
            move_selected_ball(0, hp.DEFAULT_MOVEMENT,)

        i = 0
        # interactive game loop
        while i < len(balls):
            if selected_ball_index is not None and i != selected_ball_index:
                dx = balls[i]['position'][0] - balls[selected_ball_index]['position'][0]
                dy = balls[i]['position'][1] - balls[selected_ball_index]['position'][1]
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 2 * hp.BALL_RADIUS:
                    # remove balls that the selected ball touches
                    del balls[i]

                    # Adjust selected_ball_index if necessary
                    if i < selected_ball_index:
                        selected_ball_index -= 1

                    # set the selected ball velocity to 0
                    balls[selected_ball_index]['velocity'] = [0, 0]
                    continue 
            
            # moves the ball
            move_ball(balls[i])
            i += 1

        # Loop through all the balls and bounce them off each other if applicable
        for j in range(len(balls)):
            for k in range(j + 1, len(balls)):
                # if the ball is the selected ball, don't bounce it
                if selected_ball_index is not None and (j == selected_ball_index or k == selected_ball_index):
                    continue
                
                bounce_balls(balls[j], balls[k])

        # Draw the balls onto the window
        for ball in balls:
            draw_ball(ball)

        # if the selected ball is the only ball left, win game and exit
        if selected_ball_index is not None and len(balls) == 1:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # quits the game if the game is no longer "running"
    pygame.quit()

if __name__ == "__main__":
    main()

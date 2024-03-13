import pygame
import random as rand
import math
import hyperparameter as hp
import psutil
import main 

# list of balls currently on the screen
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
def addBall(clickPosition, balls, velocity, radius):
    newBall = {
        'position': list(clickPosition),
        # 'velocity': [rand.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY), rand.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY)],
        # set velocity to either positive or negative velocity
        'velocity': [rand.choice([-1, 1]) * velocity, rand.choice([-1, 1]) * velocity],
        'color': (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)),
        'radius': radius
    }
    balls.append(newBall)
    
"""
Checks if the click is on a ball.

Parameters:
- clickPosition: The position of the click on the screen.
"""
def isClickOnBall(clickPosition, balls):
    for ball in balls:
        ballDistanceFromClick = getDistanceClickBall(clickPosition, ball)
        
        if ballDistanceFromClick < ball['radius']:
            return True
    return False

"""
Moves the ball given its velocity and position.

Parameters:
- ball: The ball to move.
"""

def moveBall(ball):    
    ball['position'][0] += ball['velocity'][0]
    ball['position'][1] += ball['velocity'][1]

    # Check boundary conditions: If true, Bounce off walls
    if ball['position'][0] <= ball['radius'] or ball['position'][0] >= hp.WIDTH - ball['radius']:
        ball['velocity'][0] *= -1
    if ball['position'][1] <= ball['radius'] or ball['position'][1] >= hp.HEIGHT - ball['radius']:
        ball['velocity'][1] *= -1

"""
Bounces balls off each other.

Parameters:
- ball1: The first ball.
- ball2: The second ball.
"""
def bounceBalls(ball1, ball2):
    dx = ball1['position'][0] - ball2['position'][0]
    dy = ball1['position'][1] - ball2['position'][1]
    distance = math.sqrt(dx**2 + dy**2)

    # Check if balls are overlapping
    if distance < 2*ball1['radius']:
        # Calculate new velocities
        nx = dx / distance
        ny = dy / distance
        relativeVelocity = 2 * (ball1['velocity'][0] * nx + ball1['velocity'][1] * ny - ball2['velocity'][0] * nx - ball2['velocity'][1] * ny) / 2

        ball1['velocity'][0] -= relativeVelocity * nx
        ball1['velocity'][1] -= relativeVelocity * ny
        ball2['velocity'][0] += relativeVelocity * nx
        ball2['velocity'][1] += relativeVelocity * ny

        # Adjust the position of the balls so they don't overlap
        overlap = 2 * ball1['radius'] - distance
        correction_factor = overlap / distance / 2  # Divide the overlap distance between the two balls
        ball1['position'][0] += correction_factor * dx
        ball1['position'][1] += correction_factor * dy
        ball2['position'][0] -= correction_factor * dx
        ball2['position'][1] -= correction_factor * dy

"""
Returns the distance between the click and the ball.

Parameters:
- click_pos: The position of the click on the screen.
- ball: The ball to check the distance from.
"""
def getDistanceClickBall(click_pos, ball):
    return math.sqrt((ball['position'][0] - click_pos[0]) ** 2 + (ball['position'][1] - click_pos[1]) ** 2)

"""
Displays the text on the screen.

Parameters:
- text: The text to display.
- x: The x position of the text.
- y: The y position of the text.
- window: The window to display the text on.
"""
def displayText(text, x, y, window):
    font = pygame.font.Font(None, 36)
    text = font.render(text, 1, hp.TEXT_COLOR)
    textpos = text.get_rect(centerx=x, centery=y)
    window.blit(text, textpos)

# def displayText(text, x, y, gameWindow):
#     font = pygame.font.SysFont(None, 35)
#     textSurface = font.render(text, True, (255, 255, 255))  # White text
#     gameWindow.blit(textSurface, (x, y))

"""
Displays the entry screen.
"""
def displayEntryScreen(gameWindow, clock):
    entryScreen = True
    titleYPos = hp.HEIGHT / 4  # Starting Y position for the title
    startYPos = hp.HEIGHT / 3  # Starting Y position for the controls text
    increment = 30  # Incremental Y distance between each line of text

    while entryScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    entryScreen = False

        gameWindow.fill(hp.BACKGROUND_COLOR)
        displayText('Welcome to the Ball Game!', hp.WIDTH / 2, titleYPos, gameWindow)
        displayText('Controls:', hp.WIDTH / 2, startYPos, gameWindow)
        displayText('Click Screen: Add ball', hp.WIDTH / 2, startYPos + increment, gameWindow)
        displayText('Click Ball: Select it', hp.WIDTH / 2, startYPos + increment * 2, gameWindow)
        displayText('Arrow Keys: Move Selection', hp.WIDTH / 2, startYPos + increment * 3, gameWindow)
        displayText('1/2: Slower/Faster Balls', hp.WIDTH / 2, startYPos + increment * 4, gameWindow)
        displayText('60 seconds to remove all other balls through collision', hp.WIDTH / 2, startYPos + increment * 6, gameWindow)
        displayText('Press SPACE to start', hp.WIDTH / 2, startYPos + increment * 7, gameWindow)
        pygame.display.update()
        clock.tick(15)

"""
Displays the ending screen.
"""
def displayEndingScreen(gameWindow, clock, score):  # Pass the calculated score as an argument
    endingScreen = True
    while endingScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    endingScreen = False

        gameWindow.fill(hp.BACKGROUND_COLOR)
        displayText('Game Over!', hp.WIDTH / 2, hp.HEIGHT / 3, gameWindow)
        displayText('Score: ' + str(score*100), hp.WIDTH / 2, hp.HEIGHT / 2, gameWindow)  # Display the constant score
        displayText('Press SPACE to quit.', hp.WIDTH / 2, hp.HEIGHT - 120, gameWindow)
        pygame.display.update()
        clock.tick(15)
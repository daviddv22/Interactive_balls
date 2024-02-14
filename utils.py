import pygame
import random as rand
import math
import hyperparameter as hp
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
def addBall(clickPosition, balls):
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
def isClickOnBall(clickPosition, balls):
    for ball in balls:
        ballDistanceFromClick = getDistanceClickBall(clickPosition, ball)
        
        if ballDistanceFromClick < hp.BALL_RADIUS:
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
def bounceBalls(ball1, ball2):
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
Returns the distance between the click and the ball.

Parameters:
- click_pos: The position of the click on the screen.
- ball: The ball to check the distance from.
"""
def getDistanceClickBall(click_pos, ball):
    return math.sqrt((ball['position'][0] - click_pos[0]) ** 2 + (ball['position'][1] - click_pos[1]) ** 2)
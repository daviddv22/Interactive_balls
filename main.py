import pygame
import random as rand
import math
import hyperparameter as hp
import utils

# ************************************************** GLOBAL INITIALIZATIONS ******************************************
# Initialize pygame variables
pygame.init()
gameWindow = pygame.display.set_mode((hp.WIDTH, hp.HEIGHT))

# player ball index (selected ball)
SELECTED_BALL_INDEX = None

# list of balls currently on the screen
balls = []

# Game loop setup
running = True
clock = pygame.time.Clock()
# ********************************************************************************************************************

"""
Draws the ball onto the gameWindow.

Parameters:
- ball: The ball to draw.
"""
def drawBall(ball):
    pygame.draw.circle(gameWindow, ball['color'], (int(ball['position'][0]), int(ball['position'][1])), hp.BALL_RADIUS)

"""
Selects the ball if the click is on a ball.

Parameters:
- click_pos: The position of the click on the screen.
"""
def selectBall(click_pos, balls):
    global SELECTED_BALL_INDEX
    for i, ball in enumerate(balls):
        distance = utils.getDistanceClickBall(click_pos, ball)
        if distance < hp.BALL_RADIUS:
            SELECTED_BALL_INDEX = i

            # stop the ball from moving so the user knows they have selected it
            balls[SELECTED_BALL_INDEX]['velocity'] = [0, 0]
            break

"""
Moves the selected ball in the inputted direction.

Parameters:
- dx: The change in the x direction.
- dy: The change in the y direction.
"""
def moveSelectedBall(dx, dy, balls):
    if SELECTED_BALL_INDEX is not None:
        # screen boundaries conditions
        ballXPos = balls[SELECTED_BALL_INDEX]['position'][0]
        ballYPos = balls[SELECTED_BALL_INDEX]['position'][1]
        if ballXPos + dx < hp.BALL_RADIUS or \
            ballXPos + dx > hp.WIDTH - hp.BALL_RADIUS:
            dx = 0
        if ballYPos + dy < hp.BALL_RADIUS or \
            ballYPos + dy > hp.HEIGHT - hp.BALL_RADIUS:
            dy = 0
    
        # move the ball
        balls[SELECTED_BALL_INDEX]['position'][0] += dx
        balls[SELECTED_BALL_INDEX]['position'][1] += dy

"""
Deletes the selected ball.
"""
def deleteSelectedBall(balls):
    if SELECTED_BALL_INDEX is not None:
        del balls[SELECTED_BALL_INDEX]
        SELECTED_BALL_INDEX = None
# ************************************************** MAIN FUNCTION **************************************************
def main():
    global running, SELECTED_BALL_INDEX, balls

    # Initialize balls given the initial settings
    for _ in range(hp.START_NUM_BALLS):
        utils.addBall([rand.randint(hp.BALL_RADIUS, hp.WIDTH - hp.BALL_RADIUS), rand.randint(hp.BALL_RADIUS, hp.HEIGHT - hp.BALL_RADIUS)], balls)
        

    while running:
        gameWindow.fill(hp.BACKGROUND_COLOR)

        # input handling
        for event in pygame.event.get():
            # if the user closes the gameWindow, exit the game
            if event.type == pygame.QUIT:
                running = False

            # if the user clicks on the screen, add a ball if the click is not on a ball
            # otherwise, select the ball that was clicked on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not utils.isClickOnBall(event.pos, balls):
                    utils.addBall(event.pos, balls)
                else:
                    selectBall(event.pos, balls)
            
            # if the user presses the delete key, delete the selected ball
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    deleteSelectedBall(balls)

        # define the movement of the selected ball based on the user's input through the arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            moveSelectedBall(-hp.DEFAULT_MOVEMENT, 0, balls)
        if keys[pygame.K_RIGHT]:
            moveSelectedBall(hp.DEFAULT_MOVEMENT, 0, balls)
        if keys[pygame.K_UP]:
            moveSelectedBall(0, -hp.DEFAULT_MOVEMENT, balls)
        if keys[pygame.K_DOWN]:
            moveSelectedBall(0, hp.DEFAULT_MOVEMENT, balls)

        i = 0
        # interactive game loop
        while i < len(balls):
            if SELECTED_BALL_INDEX is not None and i != SELECTED_BALL_INDEX:
                dx = balls[i]['position'][0] - balls[SELECTED_BALL_INDEX]['position'][0]
                dy = balls[i]['position'][1] - balls[SELECTED_BALL_INDEX]['position'][1]
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 2 * hp.BALL_RADIUS:
                    # remove balls that the selected ball touches
                    del balls[i]

                    # Adjust selected_ball_index if necessary
                    if i < SELECTED_BALL_INDEX:
                        SELECTED_BALL_INDEX -= 1

                    # set the selected ball velocity to 0
                    balls[SELECTED_BALL_INDEX]['velocity'] = [0, 0]
                    continue 
            
            # moves the ball
            utils.moveBall(balls[i])
            i += 1

        # Loop through all the balls and bounce them off each other if applicable
        for j in range(len(balls)):
            for k in range(j + 1, len(balls)):
                # if the ball is the selected ball, don't bounce it
                if SELECTED_BALL_INDEX is not None and (j == SELECTED_BALL_INDEX or k == SELECTED_BALL_INDEX):
                    continue

                utils.bounceBalls(balls[j], balls[k])

        # Draw the balls onto the gameWindow
        for ball in balls:
            drawBall(ball)

        # if the selected ball is the only ball left, win game and exit
        if SELECTED_BALL_INDEX is not None and len(balls) == 1:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # quits the game if the game is no longer "running"
    pygame.quit()

if __name__ == "__main__":
    main()

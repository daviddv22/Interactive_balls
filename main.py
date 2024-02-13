import pygame
import random
import math
import hyperparameter as hp



# Initialize pygame variables
pygame.init()
window = pygame.display.set_mode((hp.WIDTH, hp.HEIGHT))
selected_ball_index = None  # Keep track of the selected ball
balls = []

# Game loop setup
running = True
clock = pygame.time.Clock()

# Ball Functions

# add the ball to the screen with a click
def add_ball(position):
    ball = {
        'position': list(position),
        'velocity': [random.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY), random.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY)],
        'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    }
    balls.append(ball)

# check if the click is on a ball
def is_click_on_ball(click_pos):
    for ball in balls:
        distance = math.sqrt((ball['position'][0] - click_pos[0]) ** 2 + (ball['position'][1] - click_pos[1]) ** 2)
        if distance < hp.BALL_RADIUS:
            return True
    return False

# move the selected ball in the inputted direction
def move_selected_ball(dx, dy):
    if selected_ball_index is not None:
        # prevent the ball from going off the screen
        if balls[selected_ball_index]['position'][0] + dx < hp.BALL_RADIUS or balls[selected_ball_index]['position'][0] + dx > hp.WIDTH - hp.BALL_RADIUS:
            dx = 0
        if balls[selected_ball_index]['position'][1] + dy < hp.BALL_RADIUS or balls[selected_ball_index]['position'][1] + dy > hp.HEIGHT - hp.BALL_RADIUS:
            dy = 0
        balls[selected_ball_index]['position'][0] += dx
        balls[selected_ball_index]['position'][1] += dy

# remove the selected ball
def delete_selected_ball():
    if selected_ball_index is not None:
        del balls[selected_ball_index]

# select the ball if the click is on a ball
def select_ball(click_pos):
    global selected_ball_index
    selected_ball_index = None
    for i, ball in enumerate(balls):
        distance = math.sqrt((ball['position'][0] - click_pos[0]) ** 2 + (ball['position'][1] - click_pos[1]) ** 2)
        if distance < hp.BALL_RADIUS:
            selected_ball_index = i
            # set velocity to 0
            balls[selected_ball_index]['velocity'] = [0, 0]
            break

# Move the ball
def move_ball(ball):
    ball['position'][0] += ball['velocity'][0]
    ball['position'][1] += ball['velocity'][1]
    # Bounce off walls
    if ball['position'][0] <= hp.BALL_RADIUS or ball['position'][0] >= hp.WIDTH - hp.BALL_RADIUS:
        ball['velocity'][0] *= -1
    if ball['position'][1] <= hp.BALL_RADIUS or ball['position'][1] >= hp.HEIGHT - hp.BALL_RADIUS:
        ball['velocity'][1] *= -1

# Bounce balls off each other
def bounce_balls(ball1, ball2):
    dx = ball1['position'][0] - ball2['position'][0]
    dy = ball1['position'][1] - ball2['position'][1]
    distance = math.sqrt(dx**2 + dy**2)

    # Check if balls are overlapping
    if distance < 2*hp.BALL_RADIUS:
        # Calculate new velocities
        nx = dx / distance
        ny = dy / distance
        p = 2 * (ball1['velocity'][0] * nx + ball1['velocity'][1] * ny - ball2['velocity'][0] * nx - ball2['velocity'][1] * ny) / 2
        ball1['velocity'][0] -= p * nx
        ball1['velocity'][1] -= p * ny
        ball2['velocity'][0] += p * nx
        ball2['velocity'][1] += p * ny

        overlap = 2 * BALL_RADIUS - distance
        correction_factor = overlap / distance / 2  # Divide the overlap distance between the two balls
        ball1['position'][0] += correction_factor * dx
        ball1['position'][1] += correction_factor * dy
        ball2['position'][0] -= correction_factor * dx
        ball2['position'][1] -= correction_factor * dy

# Draw the ball
def draw_ball(ball):
    pygame.draw.circle(window, ball['color'], (int(ball['position'][0]), int(ball['position'][1])), hp.BALL_RADIUS)

def main():
    global running, selected_ball_index, balls
    # Colors and ball settings

    # Initialize balls
    for _ in range(hp.START_NUM_BALLS):
        # set the ball's position, velocity, and color
        ball = {
            'position': [random.randint(hp.BALL_RADIUS, hp.WIDTH - hp.BALL_RADIUS), random.randint(hp.BALL_RADIUS, hp.HEIGHT - hp.BALL_RADIUS)],
            'velocity': [random.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY), random.randint(-hp.MAX_VELOCITY, hp.MAX_VELOCITY)],
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        }

        # add the ball to the list of balls
        balls.append(ball)
        

    while running:
        # input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not is_click_on_ball(event.pos):
                    add_ball(event.pos)
                else:
                    select_ball(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    delete_selected_ball()
                    selected_ball_index = None

        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        if keys[pygame.K_LEFT]:
            move_selected_ball(-10, 0)
        if keys[pygame.K_RIGHT]:
            move_selected_ball(10, 0)
        if keys[pygame.K_UP]:
            move_selected_ball(0, -10)
        if keys[pygame.K_DOWN]:
            move_selected_ball(0, 10)

        window.fill(hp.BACKGROUND_COLOR)

        i = 0
        # interactive game loop
        while i < len(balls):
            if selected_ball_index is not None and i != selected_ball_index:
                dx = balls[i]['position'][0] - balls[selected_ball_index]['position'][0]
                dy = balls[i]['position'][1] - balls[selected_ball_index]['position'][1]
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 2 * hp.BALL_RADIUS:
                    del balls[i]  # Remove the touched ball
                    # Adjust selected_ball_index if necessary
                    if i < selected_ball_index:
                        selected_ball_index -= 1
                    # set the selected ball velocity to 0
                    balls[selected_ball_index]['velocity'] = [0, 0]
                    continue  # Skip the rest of the loop to avoid incrementing i
                    
            move_ball(balls[i])
            i += 1

        # Bounce balls off each other
        for j in range(len(balls)):
            for k in range(j + 1, len(balls)):
                # if the ball is the selected ball, don't bounce it
                if selected_ball_index is not None and (j == selected_ball_index or k == selected_ball_index):
                    continue
                bounce_balls(balls[j], balls[k])

        # Draw the balls
        for ball in balls:
            draw_ball(ball)

        pygame.display.flip()
        clock.tick(60)

        # if the selected ball is the only ball left, win game and exit
        if selected_ball_index is not None and len(balls) == 1:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame, sys, time, random

# Starting PyGame
pygame.init()

# Setting non-mutable variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREY = (220, 220, 220)
FPS = 5

# Setting mutable variables
# Snake variables
snake_x = SCREEN_WIDTH // 2
snake_y = SCREEN_HEIGHT // 2
snake_x_change, snake_y_change = 0, 0
SNAKE_WIDTH, SNAKE_HEIGHT = 10, 10

# Food variables
food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_WIDTH) / 10.0) * 10.0
food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_HEIGHT) / 10.0) * 10.0

# Setting pygame objects
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption(___)  # TODO 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
score = 0

# Defining a function
# def ___: # TODO 12
#     score_val = font.render("Your score: " + str(score), True, COLOR_GREY)
#     screen.blit(___, (0,0)) # TODO 13

# Creating our game loop
while True:
    # Looping through events
    for event in pygame.event.get():
        # Quitting event
        if event.type == pygame.QUIT:
            sys.exit()
        # Keypress event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_x_change = 0
                snake_y_change = -SNAKE_HEIGHT
            # elif event.key == pygame.K_DOWN:  # uncomment after finishing below # TODO 3
            #     snake_x_change = 0
            #     snake_y_change = ___ # TODO 3
            # elif event.key == pygame.K_RIGHT:  # uncomment after finishing below
            #     snake_x_change = ___  # TODO 4
            #     snake_y_change = ___  # TODO 5
            # elif event.key == pygame.K_LEFT:  # TODO 6
            #     snake_x_change = ___  # TODO 7
            #     snake_y_change = ___  # TODO 8

    # Updating snake position
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Rendering our screen
    # screen.fill(___)  # TODO 1
    # pygame.draw.rect(screen, COLOR_BLUE,
    #                  [___, ___, SNAKE_WIDTH, SNAKE_HEIGHT])  # TODO 2
    pygame.draw.rect(screen, COLOR_BLACK,
                     [snake_x, snake_y, SNAKE_WIDTH, SNAKE_HEIGHT])

    # Handling our food being eaten
    # if snake_x == ___ and ___ == food_y:  # TODO 10
    #     food_x = round(
    #         random.randrange(0, SCREEN_WIDTH - SNAKE_WIDTH) / 10.0) * 10.0
    #     food_y = round(
    #         random.randrange(0, SCREEN_HEIGHT - SNAKE_HEIGHT) / 10.0) * 10.0
    #     score = score + ___  # TODO 11

    # Handling game over
    if snake_x >= SCREEN_WIDTH or snake_x < 0 or snake_y >= SCREEN_HEIGHT or snake_y < 0:
        break

    # display_score(score) # uncomment after finishing TODO 12 and TODO 13
    pygame.display.update()
    clock.tick(FPS)

# Displaying game over
# message = font.render(___, True, COLOR_RED)  # TODO 9
screen.fill((255, 255, 255))
# screen.blit(message,
#             (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))  # uncomment after TODO 9
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()

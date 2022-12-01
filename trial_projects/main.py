import pygame, sys, time, random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREY = (220, 220, 220)

snake_x = SCREEN_WIDTH // 2
snake_y = SCREEN_HEIGHT // 2
snake_x_change, snake_y_change = 0, 0
SNAKE_WIDTH, SNAKE_HEIGHT = 10, 10

food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_WIDTH) / 10.0) * 10.0
food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_HEIGHT) / 10.0) * 10.0

FPS = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
score = 0

def display_score(score):
    score_val = font.render("Your score: " + str(score), True, COLOR_GREY)
    screen.blit(score_val, [0, 0])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_x_change = 0
                snake_y_change = -SNAKE_HEIGHT
            elif event.key == pygame.K_DOWN:
                snake_x_change = 0
                snake_y_change = SNAKE_HEIGHT
            elif event.key == pygame.K_RIGHT:
                snake_x_change = SNAKE_WIDTH
                snake_y_change = 0
            elif event.key == pygame.K_LEFT:
                snake_x_change = -SNAKE_WIDTH
                snake_y_change = 0

    snake_x += snake_x_change
    snake_y += snake_y_change
    screen.fill(COLOR_WHITE)
    pygame.draw.rect(screen, COLOR_BLUE, [food_x, food_y, SNAKE_WIDTH, SNAKE_HEIGHT])
    pygame.draw.rect(screen, COLOR_BLACK, [snake_x, snake_y, SNAKE_WIDTH, SNAKE_HEIGHT])

    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_WIDTH) / 10.0) * 10.0
        food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_HEIGHT) / 10.0) * 10.0
        score += 1

    if snake_x >= SCREEN_WIDTH or snake_x < 0 or snake_y >= SCREEN_HEIGHT or snake_y < 0:
        break
    
    display_score(score)
    pygame.display.update()
    clock.tick(FPS)


message = font.render("Game Over", True, COLOR_RED)
screen.fill((255, 255, 255))
screen.blit(message, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()

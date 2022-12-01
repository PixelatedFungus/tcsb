from turtle import window_height
import pygame
import os

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
# SPACESHIP_WIDTH = 55
# SPACESHIP_HEIGHT = 40
FPS = 30

pygame.init()
window = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Turnip")
clock = pygame.time.Clock()

# Scaling and rotating the yellow spaceship sprite
yellowspaceshipimg = pygame.image.load(
    os.path.join(".", "spaceship-yellow.png"))
yellowspaceshipimg = pygame.transform.scale(
    yellowspaceshipimg, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
yellowspaceshipimg = pygame.transform.rotate(yellowspaceshipimg, 180)

# Scaling and rotating the red spaceship sprite
redspaceshipimg = pygame.image.load(os.path.join(".", "spaceship-red.png"))
redspaceshipimg = pygame.transform.scale(redspaceshipimg,
                                         (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
redspaceshipimg = pygame.transform.rotate(redspaceshipimg, 180)


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, sprite, spaceship_location, spaceship_dimension, spaceship_scale):
        self.sprite = sprite
        self.spaceship_width = spaceship_dimension[0]
        self.spaceship_height = spaceship_dimension[1]
        self.spaceship_scale = spaceship_scale
        self.rect = pygame.Rect(spaceship_location[0], spaceship_location[1], self.spaceship_width * self.spaceship_scale, self.spaceship_height * self.spaceship_scale)
        self.acc = 0.75
        self.vel_x = 0
        self.vel_y = 0
        self.move_x = 0 # possible values: -1, 0, 1. -1: moving left, 1: moving right, 0: not moving on x-axis
        self.move_y = 0 # possible values: -1, 0, 1. -1: moving up, 1: moving down, 0: not moving on y_axis
    
    def draw(self):
        window.blit(self.sprite, (self.rect.x, self.rect.y))
        
    def move(self, tiles):
        collision_sides = {'top': False, 'bottom': False, 'right': False, 'left': False}
        # acceleration math
        if self.move_x == 0 and self.vel_x < 0:
            self.vel_x += self.acc
        if self.move_x == 0 and self.vel_x > 0:
            self.vel_x -= self.acc
        elif self.move_x == -1:
            self.vel_x -= self.acc
        elif self.move_x == 1:
            self.vel_x += self.acc
        
        if self.move_y == 0 and self.vel_y < 0:
            self.vel_y += self.acc
        elif self.move_y == 0 and self.vel_y > 0:
            self.vel_y -= self.acc
        elif self.move_y == -1:
            self.vel_y -= self.acc
        elif self.move_y == 1:
            self.vel_y += self.acc
        # check collisions along the x-axis
        self.rect.x += self.vel_x
        collisions = self.check_collisions(tiles)
        for tile in collisions:
            if self.vel_x > 0:
                self.rect.right = tile.left
                collision_sides['right'] = True
            elif self.vel_x < 0:
                self.rect.left = tile.right
                collision_sides['left'] = True

        # check to see if we have hit the left or right edge
        if self.rect.x < 0:
            self.rect.x = 0
            self.vel_x = 0
        elif self.rect.x + self.spaceship_width > window.get_width():
            self.rect.x = window.get_width() - self.spaceship_width
            self.vel_x = 0

        # check collisions along the y-axis
        self.rect.y += self.vel_y
        collisions = self.check_collisions(tiles)
        for tile in collisions:
            if self.vel_y > 0:
                self.rect.bottom = tile.top
                collision_sides['bottom'] = True
            elif self.vel_y < 0:
                self.rect.top = tile.bottom
                collision_sides['top'] = True
        
        # check to see if we have hit the top or bottom edge
        if self.rect.y < 0:
            self.rect.y = 0
            self.vel_y = 0
        elif self.rect.y + self.spaceship_height > window.get_height():
            self.rect.y = window.get_height() - self.spaceship_height
            self.vel_y = 0
        
        return collision_sides

    def check_collisions(self, tiles):
        return []

def draw_window(sprites):
    """
    Input:
        sprites
    Output:
        Nothing

    This function takes in the rectangles for the sprites we want to draw and draws them using window.blit. The first line draws our background and fills it with the color white.
    """
    window.fill((255, 255, 255))
    for sprite in sprites:
        sprite.draw()

def event_handler(events, run, yellowShip, redShip):
    for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    yellowShip.move_y = -1
                if event.key == pygame.K_s:
                    yellowShip.move_y = 1
                if event.key == pygame.K_a:
                    yellowShip.move_x = -1
                if event.key == pygame.K_d:
                    yellowShip.move_x = 1
                if event.key == pygame.K_UP:
                    redShip.move_y = -1
                if event.key == pygame.K_DOWN:
                    redShip.move_y = 1
                if event.key == pygame.K_RIGHT:
                    redShip.move_x = 1
                if event.key == pygame.K_LEFT:
                    redShip.move_x = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    yellowShip.move_y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    yellowShip.move_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    redShip.move_y = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    redShip.move_x = 0
    return run


def main():
    run = True
    yellowShip = Spaceship(yellowspaceshipimg, (50, 50), (yellowspaceshipimg.get_width(), yellowspaceshipimg.get_height()), 1)
    redShip = Spaceship(redspaceshipimg, (60, 50), (redspaceshipimg.get_width(), redspaceshipimg.get_height()), 1)
    sprite_list = [yellowShip, redShip]
    while run:
        run = event_handler(pygame.event.get(), run, yellowShip, redShip)
        
        window.fill((255, 255, 255))
        draw_window(sprite_list)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()

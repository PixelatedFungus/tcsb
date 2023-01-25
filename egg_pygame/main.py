import pygame, sys
from Sprite import Egg, Map
from Utils import loadImage, readMap


SCREEN_SIZE = (320, 320)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
SPRITE_SIZE = (32, 32)
FPS = 30
PLAYER_START = ((SCREEN_SIZE[0] - SPRITE_SIZE[0]) // 2, (SCREEN_SIZE[1] - SPRITE_SIZE[1]) // 2)
OFFSET_START = (0, 0)

player_img = loadImage("egg")
block_img = loadImage("block")
map_matrix = readMap("map")

blocks = Map(5, map_matrix, SCREEN, block_img, SPRITE_SIZE)
player = Egg(SCREEN, player_img, SPRITE_SIZE, PLAYER_START)
clock = pygame.time.Clock()

offset = list(OFFSET_START)

def main():
    while True:
        SCREEN.fill((255, 255, 255))
        block_list = blocks.draw(offset)
        player.draw(0, offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.move_right = True
                elif event.key == pygame.K_a:
                    player.move_left = True
                elif event.key == pygame.K_SPACE:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.move_right = False
                elif event.key == pygame.K_a:
                    player.move_left = False
                elif event.key == pygame.K_SPACE:
                    player.jump = False

        player.move(block_list)
        # offset[0] += (player.rect.x - offset[0] - PLAYER_START[0]) / 20
        # offset[1] += (player.rect.y - offset[1] - PLAYER_START[1]) / 20
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()
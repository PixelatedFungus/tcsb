import pygame, sys
from Player import Player
from Utils import loadImages, readMap

WINDOW_SIZE = (640, 640)
GAME_MAP = readMap("map")

pygame.init()
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
CLOCK = pygame.time.Clock()
FPS = 30


cube_img = pygame.image.load(loadImages("cube"))
spike_img = pygame.image.load(loadImages("spike"))
player_img = pygame.image.load(loadImages("player"))
player_surface = pygame.Surface((64, 64))
pygame.transform.scale(player_img, (64, 64), player_surface)
player = Player(player_surface, (64, 64), start_pos=(10, 0))

def main():
    scroll = 0
    while True:
        BLOCKS = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player.jump()
        row = 0
        column = 0
        WINDOW.fill((155, 33, 237))
        while row < len(GAME_MAP):
            while column < len(GAME_MAP[0]): 
                if GAME_MAP[row][column] == 2:
                    WINDOW.blit(spike_img, (column * 64 - scroll, row * 64))
                elif GAME_MAP[row][column] == 1:
                    WINDOW.blit(cube_img, (column * 64 - scroll, row * 64))
                if GAME_MAP[row][column] != 0:
                    BLOCKS[((column * 64 - scroll, row * 64), (64, 64))] = GAME_MAP[row][column]
                column += 1
            column = 0
            row += 1
        player.move(BLOCKS)
        player.draw(WINDOW)
        scroll += 10
        CLOCK.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
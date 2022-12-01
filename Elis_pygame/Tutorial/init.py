import pygame, os, sys
from pygame.locals import QUIT

screenWidth = 320
screenHeight = 320
timer = None
window = None
fps = 15
imageFolder = os.path.join(".", "content", "graphics")
def combine_path(path, fileName, suffix):
    """
    Input:
        path: file location
        fileName: name of the file
        suffix: type of file (png, pdf, jpeg, etc.)
    Returns the complete path of our file
    """
    return os.path.join(path, fileName + "." + suffix)
imgGrass = pygame.image.load(combine_path(imageFolder, "grass", "png"))
imgGirl = pygame.image.load(combine_path(imageFolder, "girl", "png"))
imgBunny = pygame.image.load(combine_path(imageFolder, "bunny", "png"))

def InitPygame(screenWidth, screenHeight):
    global window
    global timer

    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Testing out PyGame!")


InitPygame(screenWidth, screenHeight)

class Character(pygame.sprite.Sprite):
    def __init__(self, spritesheet, spriteSize):
        self.spriteWidth = spriteSize[0]
        self.spriteHeight = spriteSize[1]
        self.spritesheet = spritesheet
        self.direction = 2 # facing towards the player
        self.velocity = 4
        self.x = 0
        self.y = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.velocity
            self.direction = 0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.velocity
            self.direction = 2
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
            self.direction = 3
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
            self.direction = 1
    
    def stop(self, key_let_go):
        if key_let_go == pygame.K_w or key_let_go == pygame.K_UP:
            self.direction = 0
        if key_let_go == pygame.K_s or key_let_go == pygame.K_DOWN:
            self.direction = 2
        if key_let_go == pygame.K_a or key_let_go == pygame.K_LEFT:
            self.direction = 1
        if key_let_go == pygame.K_d or key_let_go == pygame.K_RIGHT:
            self.direction = 3


girlCharacter = Character(imgGirl, (32, 48))
bunnyCharacter = Character(imgBunny, (32, 32))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            bunnyCharacter.move()
            girlCharacter.move()
        if event.type == pygame.KEYUP:
            print(event.key)
            bunnyCharacter.stop(event.key)
            girlCharacter.stop(event.key)


    pygame.display.update()
    timer.tick(fps)

import pygame, os
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
done = False
bgColor = pygame.Color(231, 181, 100)
frameWidth = 32
frameHeight = 48
frame = pygame.Rect(2 * frameWidth, 2 * frameHeight, frameWidth, frameHeight)


class Character(pygame.sprite.Sprite):

    def __init__(self, screen, image, imageSize, frameSize, canJump, scale):
        # The screen where this character will be drawn
        self.screen = screen
        # The scale of the character image
        self.size = [100, 100]
        # The starting x location of the character
        self.x = 160
        # The starting y location of the character
        self.y = 160
        self.velocity = 4
        self.frameWidth = frameSize[0] * scale
        self.frameHeight = frameSize[1] * scale
        self.image = pygame.transform.scale(
            image, (scale * imageSize[0], scale * imageSize[1]))
        self.position = pygame.Rect(self.x, self.y, self.frameWidth,
                                    self.frameHeight)
        self.frame = pygame.Rect(1 * self.frameWidth, 0 * self.frameHeight,
                                 self.frameWidth, self.frameHeight)
        self.hAxis = 0
        self.vAxis = -1
        self.direction = 0
        self.column_frame = 0
        self.is_walking = False
        self.canJump = canJump

    def arrow_directions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.velocity
            self.vAxis = 1
            self.hAxis = 0
        if keys[pygame.K_DOWN]:
            self.y += self.velocity
            self.vAxis = -1
            self.hAxis = 0
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
            self.vAxis = 0
            self.hAxis = 1
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
            self.vAxis = 0
            self.hAxis = -1

    def WASD_directions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.velocity
            self.vAxis = 1
            self.hAxis = 0
        if keys[pygame.K_s]:
            self.y += self.velocity
            self.vAxis = -1
            self.hAxis = 0
        if keys[pygame.K_d]:
            self.x += self.velocity
            self.vAxis = 0.5
            self.hAxis = 1
        if keys[pygame.K_a]:
            self.x -= self.velocity
            self.vAxis = 0.5
            self.hAxis = -1
    
    def WASD_KEYUP(self, event_type):
        
        def nested():
            if event_type == pygame.K_w:
                self.column_frame = 2
            if event_type == pygame.K_a:
                self.column_frame = 1
            if event_type == pygame.K_s:
                self.column_frame = 3
            if event_type == pygame.K_d:
                self.column_frame = 0
        return nested

    def draw(self, function, crop=True):
        function()
        
        self.position = pygame.Rect(self.x, self.y, frameWidth, frameHeight)
        if crop:
            if (self.vAxis == -1):
                self.direction = 0
            if (self.vAxis == 1):
                self.direction = 1
            if (self.hAxis == -1):
                self.direction = 2
            if (self.hAxis == 1):
                self.direction = 3
        else:
            self.direction = 0
        self.frame = pygame.Rect(self.column_frame * self.frameWidth,
                                self.direction * self.frameHeight,
                                self.frameWidth, self.frameHeight)
        window.blit(self.image, self.position, self.frame)
        # else:
        #     self.position = pygame.Rect(self.x, self.y, frameWidth, frameHeight)
        #     self.frame = pygame.Rect(self.column_frame * self.frameWidth, )
        #     window.blit(self.image, )

    def isWalking(self):
        if (sum(pygame.key.get_pressed()) != 0):
            return True
        else:
            return False

    def isArrow(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[
                pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            return True
        else:
            return False

    def isWASD(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[
                pygame.K_d]:
            return True
        else:
            return False


def InitPygame(screenWidth, screenHeight):
    global window
    global timer

    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Testing out PyGame!")


InitPygame(screenWidth, screenHeight)

girlCharacter = Character(window, imgGirl,
                          (128, 192), (32, 48), False, 1)
bunnyCharacter = Character(window, imgBunny, (128, 160),
                           (32, 32), True, 3)

while done == False:
    window.fill(bgColor)
    bunny_function = bunnyCharacter.WASD_directions
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if girlCharacter.isWalking() and girlCharacter.isArrow():
                girlCharacter.column_frame = (girlCharacter.column_frame + 1) % 3
            if bunnyCharacter.isWalking() and bunnyCharacter.isWASD():
                bunnyCharacter.column_frame = (bunnyCharacter.column_frame + 1) % 4
        if event.type == pygame.KEYUP:
            bunny_function = bunnyCharacter.WASD_KEYUP(event.type)

    window.blit(imgGrass, imgGrass.get_rect())
    girlCharacter.draw(girlCharacter.arrow_directions)
    bunnyCharacter.draw(bunny_function)

    if girlCharacter.isWalking() and girlCharacter.isArrow():
        girlCharacter.column_frame = (girlCharacter.column_frame + 1) % 3
    if bunnyCharacter.isWalking() and bunnyCharacter.isWASD():
        bunnyCharacter.column_frame = (bunnyCharacter.column_frame + 1) % 4

    pygame.display.update()
    timer.tick(fps)

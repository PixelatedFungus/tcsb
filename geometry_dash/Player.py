import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, dimensions: tuple, start_pos: list = [0, 0]) -> None:
        self.img = img
        self.dimensions = dimensions
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.rect = self.img.get_rect()
        
        # Movement variables
        self.gravity = 2
        self.jump_vel = 27
        self.velocity = [0, 0]

        # Jump variables
        self.can_jump = False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, (self.x, self.y))

    def move(self, blocks: dict):
        collision_directions = {"top": False,
                                "right": False,
                                "bottom": False,
                                "left": False}

        # ----- VERTICAL MOVEMENT -----
        self.velocity[1] += self.gravity
        self.rect.y += self.velocity[1]

        hit_list = self.checkCollision(blocks)
        for block_coordinates in hit_list:
            block_rect = pygame.Rect(block_coordinates[0], block_coordinates[1])
            if self.velocity[1] > 0:
                self.rect.bottom = block_rect.top
                collision_directions["bottom"] = True
            if self.velocity[1] < 0:
                self.rect.top = block_rect.bottom
                collision_directions["top"] = True
            # Checking to see if collided block is a spike
            if hit_list[block_coordinates] == 2:
                pygame.display.quit()
                sys.exit()

        if collision_directions["bottom"] == True:
            self.velocity[1] = 0
            self.can_jump = True

        self.y = self.rect.y

        # ----- HORIZONTAL MOVEMENT -----
        hit_list = self.checkCollision(blocks)
        for block_coordinates in hit_list:
            block_rect = block_rect = pygame.Rect(block_coordinates[0], block_coordinates[1])
            self.rect.right = block_rect.left
            if hit_list[block_coordinates] == 2 or hit_list[block_coordinates] == 1:
                pygame.display.quit()
                sys.exit()
        
        self.x = self.rect.x

    def jump(self):
        if self.can_jump:
            self.velocity[1] = -self.jump_vel
            self.can_jump = False

    def checkCollision(self, blocks: dict) -> dict:
        """
        Checks to see if our sprite is 
        """
        hit_list = {}
        for block_coordinates in blocks:
            block_rect = pygame.Rect(block_coordinates[0], block_coordinates[1])
            if self.rect.colliderect(block_rect):
                hit_list[block_coordinates] = blocks[block_coordinates]
        return hit_list
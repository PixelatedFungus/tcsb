import pygame

class Sprite(pygame.sprite.Sprite):
    """
    General class for any Sprite in the game.
    __init__ : fully defined
    generate_sprites : fully defined
    crop : fully defined
    draw : minimally defined
    move : not defined
    animate: not defined
    """

    def __init__(self, SCREEN: pygame.Surface, SPRITE_SHEET: pygame.Surface, DIMENSIONS: tuple, POSITION: tuple = (0, 0)):
        """
        SPRITE_SHEET: the spritesheet rendered (drawn by computer) as a surface
        DIMENSIONS: [0] - the width of each sprite, [1] - the height of each sprite
        POSITION: [0] - starting x-position, [1] - starting y-position
        """
        self.SCREEN = SCREEN
        self.SPRITE_SHEET = SPRITE_SHEET
        self.DIMENSIONS = DIMENSIONS
        self.sprite_frames = []
        self.x = POSITION[0]
        self.y = POSITION[1]
        self.generateSpriteFrames()

    def generateSpriteFrames(self) -> None:
        """
        Called by the constructor. Populates the sprite_frames list.
        """
        assert self.SPRITE_SHEET.get_height() % self.DIMENSIONS[1] == 0, "Sprite.generateSpriteFrames: Spritesheet incorrect height"
        assert self.SPRITE_SHEET.get_width() % self.DIMENSIONS[0] == 0, "Sprite.generateSpriteFrames: Spritesheet incorrect width"
        num_rows = self.SPRITE_SHEET.get_height() // self.DIMENSIONS[1]
        num_columns = self.SPRITE_SHEET.get_width() // self.DIMENSIONS[0]
        for row in range(num_rows):
            for column in range(num_columns):
                coordinates = (column * self.DIMENSIONS[0], row * self.DIMENSIONS[1])
                surface = self.crop(coordinates)
                self.sprite_frames.append(surface)
                

    def crop(self, coordinates: tuple) -> pygame.Surface:
        """
        Returns a cropped part of the spritesheet as a Surface.
        """
        frame = pygame.Rect(coordinates, self.DIMENSIONS)
        surface = pygame.Surface(self.DIMENSIONS).convert()
        surface.set_colorkey((0, 0, 0))
        surface.blit(self.SPRITE_SHEET, (0, 0), frame)
        return surface

    def draw(self, sprite_num: int, offset: tuple):
        """
        Draws a sprite from the sprite list onto the given surface.
        """
        assert 0 <= sprite_num < len(self.sprite_frames), "Sprite.draw: sprite_num out of bounds"
        chosen_sprite = self.sprite_frames[sprite_num]
        self.SCREEN.blit(chosen_sprite, (self.x - offset[0], self.y - offset[1]))


class Character(Sprite):
    def __init__(self, SCREEN: pygame.Surface, SPRITE_SHEET: pygame.Surface, DIMENSIONS: tuple, POSITION: tuple = (0, 0)):
        super().__init__(SCREEN, SPRITE_SHEET, DIMENSIONS, POSITION)
        self.rect = pygame.Rect((self.x, self.y), self.DIMENSIONS)
        self.move_left = False
        self.move_right = False
        self.movement = [0, 0]

        # Horizontal movement
        self.h_vel = 0
        self.acceleration = 0.4
        self.deceleration_factor = 2

        # Vertical movement
        self.v_vel = 0
        self.jump = False
        self.jump_vel = 8
        self.gravity = 1
        self.air_timer = 0
        self.max_fall_speed = 10

        self.collision_directions = {"top": False, "right": False, "bottom": False, "left": False}


    def move(self, collide_rects: list) -> dict:
        """
        movement[0] = the amount we want to move on the x-axis
        movement[1] = the amount we want to move on the y-axis
        """

        # Reset collision directions
        self.collision_directions = {"top": False, "right": False, "bottom": False, "left": False}
        self.movement = [0, 0]

        # ----- VERTICAL START -----

        # Move vertically to jump
        if self.air_timer < 2 and self.jump:
            self.v_vel -= self.jump_vel

        # Apply gravity
        if self.v_vel < self.max_fall_speed:
            self.v_vel += self.gravity
        # Casting the vertical velocity to int, avoids clipping
        self.movement[1] = int(self.v_vel)

        # Moving vertical axis
        self.rect.y += self.movement[1]
        block_list = self.testCollide(collide_rects)
        for block in block_list:
            if self.movement[1] > 0:
                self.rect.bottom = block.top
                self.collision_directions["bottom"] = True
            elif self.movement[1] < 0:
                self.rect.top = block.bottom
                self.collision_directions["top"] = True

        # Checking for collisions
        # TODO check for top collision
        if self.collision_directions["bottom"]:
            self.v_vel = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

        if self.collision_directions["top"]:
            self.v_vel = 0
        # ----- VERTICAL END -----

        # ----- HORIZONTAL START ----- 
        # Move horizontally and accelerate
        if -5 < self.h_vel < 5:
            if self.move_right:
                self.h_vel += self.acceleration
            if self.move_left:
                self.h_vel -= self.acceleration
            
        # Move horizontally and decelerate
        if not self.move_right and self.h_vel > 0:
            self.h_vel -= self.deceleration_factor * self.acceleration
        if not self.move_left and self.h_vel < 0:
            self.h_vel += self.deceleration_factor * self.acceleration

        # Casting the horizontal velocity to int, avoids clipping
        self.movement[0] = int(self.h_vel)
        
        # Moving horizontal axis
        self.rect.x += self.movement[0]
        block_list = self.testCollide(collide_rects)
        for block in block_list:
            if self.movement[0] > 0:
                self.rect.right = block.left
                self.collision_directions["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = block.right
                self.collision_directions["left"] = True

        # Check for horizontal collisions
        if self.collision_directions["right"] or self.collision_directions["left"]:
            self.h_vel = 0
        # ----- HORIZONTAL END -----

        self.x = self.rect.x
        self.y = self.rect.y

    def testCollide(self, collide_rects: list) -> list:
        """
        Finds collisions between self.rect and rectangles in collide_rects
        """
        block_list = []
        for block in collide_rects:
            if self.rect.colliderect(block):
                block_list.append(block)
        return block_list

    def animate(self, animation_frames: dict) -> None:
        pass

class Egg(Character):
    def __init__(self, SCREEN: pygame.Surface, SPRITE_SHEET: pygame.Surface, DIMENSIONS: tuple, POSITION: tuple = (0, 0)):
        super().__init__(SCREEN, SPRITE_SHEET, DIMENSIONS, POSITION)

class Map(Sprite):
    def __init__(self, empty: int, map_matrix: list, SCREEN: pygame.Surface, SPRITE_SHEET: pygame.Surface, DIMENSIONS: tuple, POSITION: tuple = (0, 0)):
        super().__init__(SCREEN, SPRITE_SHEET, DIMENSIONS, POSITION)
        self.map_matrix = map_matrix
        self.empty = empty

    def draw(self, offset: tuple) -> list:
        block_list = []
        y = 0
        for row in self.map_matrix:
            x = 0
            for val in row:
                location = (x * self.DIMENSIONS[0] - offset[0], y * self.DIMENSIONS[1] - offset[1])
                self.x = location[0]
                self.y = location[1]
                match val:
                    case self.empty:
                        pass
                    case other:
                        super().draw(val, offset)
                        block_list.append(pygame.Rect((self.x, self.y), self.DIMENSIONS))
                x += 1
            y += 1
        return block_list
    
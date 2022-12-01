# ----- IMPORT STATEMENTS -----
import pygame, sys, os, numpy

# Pygame initialization
pygame.init()

# ----- STATIC VARIABLES -----
# The actual display we will see on our screen
DISPLAYSIZE = (400, 300)
DISPLAYSURF = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption('Dinosaur Game')
# A smaller pygame surface that we will stretch to be the size of our display
STRETCHSIZE = (200, 150)
STRETCHSURF = pygame.Surface(STRETCHSIZE)
# Our frame rate and clock
FPS = 30
clock = pygame.time.Clock()

# ----- UTILITY FUNCTIONS -----
def load_sky(sprite_name):
    """
    Loads sprites that will be displayed in the sky
    """
    return os.path.join(".", "sprites", "sky", "sprite_" + sprite_name + ".png")

def load_dinosaur(dino_num):
    """
    Loads dinosaur character sprites
    """
    return os.path.join(".", "sprites", "dinosaur", "sprite_dinosaur" + str(dino_num) + ".png")

def load_ground(ground_num):
    """
    Loads ground sprites
    """
    return os.path.join(".", "sprites", "ground", "sprite_ground" + str(ground_num) + ".png")


dinosaur_size = (32, 32)
dinosaur_jump = pygame.image.load(load_dinosaur(0))
dinosaur_run = [
    pygame.image.load(load_dinosaur(1)),
    pygame.image.load(load_dinosaur(2))
]
dinosaur_duck = [
    pygame.image.load(load_dinosaur(3)),
    pygame.image.load(load_dinosaur(4))
]
dinosaur_lose = pygame.image.load(load_dinosaur(5))

star_r = pygame.image.load(load_sky("star_r"))
star_t = pygame.image.load(load_sky("star_t"))
moon = pygame.image.load(load_sky("moon"))
stars = [star_r, star_t]
heaven_scroll = 0.5
star_weights = [0.02, 0.98]
moon_delay = STRETCHSIZE[0] // heaven_scroll
heaven_arr = []

cloud_img = pygame.image.load(load_sky("cloud"))
cloud_scroll = 2
cloud_weights = [0.025, 0.975]
cloud_arr = []

sky_range = range(20, 50)

ground_images = [
        pygame.image.load(load_ground(0)),
        pygame.image.load(load_ground(1)),
        pygame.image.load(load_ground(2)),
        pygame.image.load(load_ground(3)),
        pygame.image.load(load_ground(4)),
        pygame.image.load(load_ground(5)),
        pygame.image.load(load_ground(6)),
        ]
ground_scroll = 5
ground_delay = 0
ground_arr = []

starting_position = STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2
dino_can_jump = True
dino_duck = False
dino_frame_delay = 1
dino_frame = 0
height = starting_position
gravity = 1 
velocity = 0


def drawDinosaur(dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height):
    """
    Picks the right dinosaur sprite(s) to draw and draws it onto the screen
    """
    # If we are on the ground
    if dino_can_jump == True:
        # If we are not ducking
        if dino_duck == False:
            STRETCHSURF.blit(dinosaur_run[dino_frame], (STRETCHSIZE[0] / 40, STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2))
        # If we are ducking
        elif dino_duck == True:
            STRETCHSURF.blit(dinosaur_duck[dino_frame], (STRETCHSIZE[0] / 40, STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2))
        # Delays our dinosaur running animation
        if dino_frame_delay == 0:
            dino_frame += 1
            dino_frame %= 2
            dino_frame_delay = 2
        else:
            dino_frame_delay -= 1
    # If we are not on the ground
    else:
        if height < starting_position:
            if dino_duck == False:
                velocity = velocity - gravity
            elif dino_duck == True:
              velocity = velocity - 2*gravity
            height -= velocity
        else:
            dino_can_jump = True
            height = starting_position
            velocity = 0
        STRETCHSURF.blit(dinosaur_jump, (STRETCHSIZE[0] / 40, height))

    return dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height


def jump(dino_can_jump, velocity, height):
    if dino_can_jump == True:
        dino_can_jump = False
        velocity = 10
        height -= velocity
    return dino_can_jump, velocity, height

def draw_clouds(cloud_arr):
    """
    Draws the clouds in the sky
    """
    # Picks a random chance of clouds being drawn
    new_cloud_chance = numpy.random.choice([True, False], p=cloud_weights)
    # len(cloud_arr) <= 3 ensure there are not too many clouds
    if len(cloud_arr) <= 3 and new_cloud_chance:
        # The x-coordinate of the cloud
        new_cloud_x = STRETCHSURF.get_width()
        # The y-coordinate of the cloud
        new_cloud_y = numpy.random.choice(sky_range)
        # Adding our new cloud to the cloud_arr
        cloud_arr.append([new_cloud_x, new_cloud_y, cloud_img])
    
    # Initializing a new_cloud_arr in order to figure out which clouds we still need to keep
    new_cloud_arr = []
    # Drawing out the clousd in the cloud array
    for cloud in cloud_arr:
        cloud_x = cloud[0]
        cloud_y = cloud[1]
        cloud_surface = cloud[2]
        STRETCHSURF.blit(cloud_surface, (cloud_x, cloud_y))
        cloud[0] -= cloud_scroll
        # If the cloud is not completely off the screen, we keep it in the new_cloud_arr
        if cloud[0] > -cloud_surface.get_width():
            new_cloud_arr.append(cloud)
    return new_cloud_arr

def draw_heaven(moon_delay, heaven_arr):
    """
    Draws out the stars and the moon
    """
    # ----- STARS START -----
    # Randomly decides whether or not we will draw a star based on star_weights 
    new_star_chance = numpy.random.choice([True, False], p=star_weights)
    if new_star_chance == True:
        # We generate a new star and choose between the two star types randomly - a twinkling star, or a non-twinkling star
        # stars[0] is the regular star, star_r
        # star[1] is the twinkling star, star_t
        new_star_choice = numpy.random.choice(stars, p=[0.5, 0.5])
        # The x-coordinate is always the same for all objects in the sky (moving from right to left)
        new_star_x = STRETCHSURF.get_width()
        # The y-coordinate is randomly generated by using the sky_range list of possible integers
        # The y-coordinate is chosen uniformly at random without weights (each height is chosen with equal chance)
        new_star_y = numpy.random.choice(sky_range)
        heaven_arr.append([new_star_x, new_star_y, new_star_choice])
    # ----- STARS END -----

    # ----- MOON START -----
    # Checks if the moon delay has reached 0
    if moon_delay == 0:
        # Takes a 50/50 chance of the moon spawning
        new_moon_chance = numpy.random.choice([True, False], p=[0.5, 0.5])
        # If the moon spawns we want to add the moon sprite to our heaven array
        if new_moon_chance == True: # I know this code is redundant, I keep it in for the students to easily understand
            new_moon_x = STRETCHSURF.get_width()
            new_moon_y = numpy.random.choice(sky_range)
            heaven_arr.append([new_moon_x, new_moon_y, moon])
        # Resets the moon_delay to the number of frames that it takes for the moon to travel across the screen
        moon_delay = STRETCHSIZE[0] // heaven_scroll
    else:
        # We decrease the moon delay every time.
        moon_delay -= 1
    # ----- MOON END -----

    new_heaven_arr = []
    for heaven in heaven_arr:
        heaven_x = heaven[0]
        heaven_y = heaven[1]
        heaven_surface = heaven[2]
        STRETCHSURF.blit(heaven_surface, (heaven_x, heaven_y))
        heaven[0] -= heaven_scroll
        if heaven[0] > -heaven_surface.get_width():
            new_heaven_arr.append(heaven)
    return moon_delay, new_heaven_arr

def drawGround(ground_delay, ground_arr):
    if ground_delay <= ground_scroll % ground_images[0].get_width():
        ground_delay = ground_images[0].get_width()
        ground_choice = numpy.random.choice(ground_images)
        ground_x = STRETCHSURF.get_width()
        ground_y = STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2
        ground_arr.append([ground_x, ground_y, ground_choice])
    ground_delay -= ground_scroll
    new_ground_arr = []
    for ground in ground_arr:
        STRETCHSURF.blit(ground[2], (ground[0], ground[1]))
        ground[0] -= ground_scroll
        if ground[0] > -ground[2].get_width(): 
            new_ground_arr.append(ground)
    return ground_delay, ground_arr

while True:
    STRETCHSURF.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                dino_can_jump, velocity, height = jump(dino_can_jump, velocity,height)
            elif event.key == pygame.K_DOWN:
                dino_duck = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                dino_duck = False

    moon_delay, heaven_arr = draw_heaven(moon_delay, heaven_arr)
    cloud_arr = draw_clouds(cloud_arr)
    ground_delay, ground_arr = drawGround(ground_delay, ground_arr)
    dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height = drawDinosaur(dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height)
    pygame.transform.scale(STRETCHSURF, DISPLAYSIZE, DISPLAYSURF)
    pygame.display.update()
    clock.tick(FPS)

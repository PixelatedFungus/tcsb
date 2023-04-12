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

def load_cacti(cacti_num):
    """
    Loads cacti sprites
    """
    return os.path.join(".", "sprites", "obstacles", "sprite_cactus" + str(cacti_num) + ".png")

def load_pterodactyl(pterodactyl_num):
    """
    Loads pterodactyl sprites
    """
    return os.path.join(".", "sprites", "obstacles", "sprite_pterodactyl" + str(pterodactyl_num) + ".png")


# Loading in dinosaur sprites
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

# Loading in heaven sprites
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

# Loading in ground images
ground_images = [
        pygame.image.load(load_ground(0)),
        pygame.image.load(load_ground(1)),
        pygame.image.load(load_ground(2)),
        pygame.image.load(load_ground(3)),
        pygame.image.load(load_ground(4)),
        pygame.image.load(load_ground(5)),
        pygame.image.load(load_ground(6))
        ]
ground_scroll = 5
ground_delay = 0
ground_arr = []

# Obstacles
obstacle_wait, obstacle_delay = 60, 60
obstacle_scroll = 5
obstacle_arr = []
cacti_images = [pygame.image.load(load_cacti(0)),
        pygame.image.load(load_cacti(1)),
        pygame.image.load(load_cacti(2)),
        pygame.image.load(load_cacti(3))]

pterodactyl_images = [pygame.image.load(load_pterodactyl(0)),
        pygame.image.load(load_pterodactyl(1))]
pterodactyl_frame_delay = 1
pterodactyl_frame_delay_SET = 5
pterodactyl_height_choices = [STRETCHSIZE[1] / 2 - int(1 * dinosaur_size[1]),
        STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2]

# Dinosaur variables
starting_position = STRETCHSIZE[1] / 2 - dinosaur_size[1] / 2
dino_can_jump = True
dino_duck = False
dino_frame_delay = 1
dino_frame = 0
height = starting_position
gravity = 1 
velocity = 0

def draw_dinosaur(dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height):
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
        if height - velocity < starting_position:
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

def draw_obstacles(obstacle_wait, obstacle_delay, obstacle_arr, obstacle_scroll, pterodactyl_frame_delay):
    if obstacle_wait == 0:
        obstacle_wait = obstacle_delay
        obstacle_choice = numpy.random.choice(['cactus', 'pterodactyl'], p=[0.7, 0.3])
        if obstacle_choice == 'cactus':
            obstacle_arr = draw_cactus(obstacle_arr)
        elif obstacle_choice == 'pterodactyl':
            obstacle_arr = draw_pterodactyl(obstacle_arr, pterodactyl_height_choices)
    else:
        obstacle_wait -= 1
    pterodactyl_frame_delay -= 1
    new_obstacle_arr = []
    for obstacle_info in obstacle_arr:
        obstacle_x = obstacle_info[0]
        obstacle_y = obstacle_info[1]
        obstacle_surface = obstacle_info[2]
        obstacle_type = obstacle_info[3]
        if (obstacle_type == 'pterodactyl'):
            if (pterodactyl_frame_delay <= 0):
                pterodactyl_frame_delay = pterodactyl_frame_delay_SET
                obstacle_surface = pterodactyl_images[obstacle_info[4]]
                obstacle_info[4] = (obstacle_info[4] + 1) % 2
            else:
                obstacle_surface = pterodactyl_images[obstacle_info[4]]
        STRETCHSURF.blit(obstacle_surface, (obstacle_x, obstacle_y))
        obstacle_info[0] -= obstacle_scroll
        if obstacle_info[0] > -obstacle_surface.get_width():
            new_obstacle_arr.append(obstacle_info)
    return obstacle_wait, new_obstacle_arr, pterodactyl_frame_delay

def draw_cactus(obstacle_arr):
    cactus_image_choice = numpy.random.choice(cacti_images)
    cactus_x = STRETCHSIZE[0]
    cactus_y = STRETCHSIZE[1] / 2 - cactus_image_choice.get_height() / 2
    obstacle_arr.append([cactus_x, cactus_y, cactus_image_choice, 'cactus'])
    return obstacle_arr

def draw_pterodactyl(obstacle_arr, pterodactyl_height_choices):
    pterodactyl_height_choice = numpy.random.choice(pterodactyl_height_choices)
    pterodactyl_x = STRETCHSIZE[0]
    pterodactyl_y = pterodactyl_height_choice
    frame = 0
    obstacle_arr.append([pterodactyl_x, pterodactyl_y, pterodactyl_images[frame], 'pterodactyl', frame])
    return obstacle_arr

def draw_ground(ground_delay, ground_arr):
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

def checkCollision(obstacle_arr):
    for obstacle_entry in obstacle_arr:
        # We create a rectangle representing the location of the dinosaur sprite
        # if we are on the floor and we are ducking and on the floor, we want to flatten the rectangle
        obstacle_rect = pygame.Rect((obstacle_entry[0], obstacle_entry[1]), (obstacle_entry[2].get_size()[0], obstacle_entry[2].get_size()[1]))

        if dino_duck and dino_can_jump:
            dinosaur_rect = pygame.Rect((STRETCHSIZE[0] / 40, height + 16), (dinosaur_size[0], dinosaur_size[1] // 2))
        else:
            dinosaur_rect = pygame.Rect((STRETCHSIZE[0] / 40 + 8, height), (dinosaur_size[0] / 2, dinosaur_size[1]))
        # pygame.draw.rect(STRETCHSURF, (0, 255, 0), dinosaur_rect)
        # pygame.draw.rect(STRETCHSURF, (255, 0, 0), obstacle_rect)
        if (dinosaur_rect.colliderect(obstacle_rect)):
            return lose()
    return height, dino_can_jump, dino_duck, velocity, heaven_arr, cloud_arr, ground_arr, obstacle_arr

def lose():
    # switch dinosaur sprite
    STRETCHSURF.blit(dinosaur_lose, (STRETCHSIZE[0] / 40, height))
    pygame.transform.scale(STRETCHSURF, DISPLAYSIZE, DISPLAYSURF)
    pygame.display.update()
    # hold position and don't do anything
    exit_loop = False
    while not exit_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                exit_loop = True
    return reset_game()

def reset_game():
    height = starting_position
    dino_can_jump = True
    dino_duck = False
    velocity = 0
    heaven_arr = []
    cloud_arr = []
    ground_arr = []
    obstacle_arr = []
    return height, dino_can_jump, dino_duck, velocity, heaven_arr, cloud_arr, ground_arr, obstacle_arr
    

while True:
    STRETCHSURF.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                dino_can_jump, velocity, height = jump(dino_can_jump, velocity, height)
            elif event.key == pygame.K_DOWN:
                dino_duck = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                dino_duck = False

    moon_delay, heaven_arr = draw_heaven(moon_delay, heaven_arr)
    cloud_arr = draw_clouds(cloud_arr)
    ground_delay, ground_arr = draw_ground(ground_delay, ground_arr)
    dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height = draw_dinosaur(dino_frame, dino_frame_delay, gravity, dino_can_jump, velocity, height)
    obstacle_wait, obstacle_arr, pterodactyl_frame_delay = draw_obstacles(obstacle_wait, obstacle_delay, obstacle_arr, obstacle_scroll, pterodactyl_frame_delay)
    height, dino_can_jump, dino_duck, velocity, heaven_arr, cloud_arr, ground_arr, obstacle_arr = checkCollision(obstacle_arr)
    pygame.transform.scale(STRETCHSURF, DISPLAYSIZE, DISPLAYSURF)
    pygame.display.update()
    clock.tick(FPS)

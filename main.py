
import pygame
import random
import json
import socket
import sys

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Shift Ultimate")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

# =========================================================
# COLORS
# =========================================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# =========================================================
# LOAD IMAGES
# =========================================================

office_image = pygame.image.load(
    "Fnaf2office.webp"
).convert()

office_image = pygame.transform.scale(
    office_image,
    (WIDTH, HEIGHT)
)

stage_image = pygame.image.load(
    "fnaf 2 stage.jpg"
).convert()

stage_image = pygame.transform.scale(
    stage_image,
    (WIDTH, HEIGHT)
)

dining_image = pygame.image.load(
    "fnaf2 dining room.webp"
).convert()

dining_image = pygame.transform.scale(
    dining_image,
    (WIDTH, HEIGHT)
)

hall_image = pygame.image.load(
    "fnaf2 hall.jpg"
).convert()

hall_image = pygame.transform.scale(
    hall_image,
    (WIDTH, HEIGHT)
)

vent_image = pygame.image.load(
    "fnaf 2 vent.jpg"
).convert()

vent_image = pygame.transform.scale(
    vent_image,
    (WIDTH, HEIGHT)
)

# =========================================================
# SAVE FILE
# =========================================================

SAVE_FILE = "save.json"

# =========================================================
# GAME STATES
# =========================================================

MENU = 0
GAME = 1
GAME_OVER = 2
WIN = 3

state = MENU

# =========================================================
# GAME VARIABLES
# =========================================================

battery = 100
night_time = 0

camera_open = False
camera_index = 0

mask_on = False

attack_timer = 0
attacking_enemy = None

mask_hold_time = 0

# =========================================================
# ROOMS
# =========================================================

rooms = [
    "Stage",
    "Dining",
    "Hall",
    "Vent",
    "Office"
]

# =========================================================
# ENEMY CLASS
# =========================================================

class Enemy:

    def __init__(self, name, aggression, color):

        self.name = name
        self.aggression = aggression
        self.position = 0
        self.cooldown = 0
        self.color = color

    def update(self, dt):

        self.cooldown += dt

        if self.cooldown >= 4:

            self.cooldown = 0

            move_roll = random.randint(1, 100)

            if move_roll <= self.aggression:

                move = random.choice([-1, 1])

                self.position += move

                self.position = max(
                    0,
                    min(len(rooms) - 1, self.position)
                )

    def room(self):
        return rooms[self.position]

    def reset(self):

        self.position = 0
        self.cooldown = 0

# =========================================================
# CREATE ENEMIES
# =========================================================

enemies = [

    Enemy("Freddy", 45, (120, 70, 20)),
    Enemy("Bonnie", 60, (80, 80, 255)),
    Enemy("Chica", 55, (255, 220, 40)),
    Enemy("Foxy", 75, (200, 40, 40))

]

# =========================================================
# SAVE SYSTEM
# =========================================================

def save_game():

    data = {

        "battery": battery,
        "night_time": night_time,
        "enemy_positions": [
            enemy.position for enemy in enemies
        ]
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)

def load_game():

    global battery
    global night_time

    try:

        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

        battery = data["battery"]
        night_time = data["night_time"]

        for i, enemy in enumerate(enemies):
            enemy.position = data["enemy_positions"][i]

        print("Save loaded")

    except:
        print("No save file found")

# =========================================================
# NETWORK FOUNDATION
# =========================================================

class Network:

    def __init__(self):

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

# =========================================================
# MENU
# =========================================================

menu_options = [
    "Start Game",
    "Load Game",
    "Quit"
]

menu_selected = 0

# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global battery
    global night_time
    global camera_open
    global camera_index
    global state

    global mask_on
    global attack_timer
    global attacking_enemy
    global mask_hold_time

    battery = 100
    night_time = 0

    camera_open = False
    camera_index = 0

    mask_on = False
    attack_timer = 0
    attacking_enemy = None
    mask_hold_time = 0

    for enemy in enemies:
        enemy.reset()

    state = MENU

# =========================================================
# DRAW MENU
# =========================================================

def draw_menu():

    screen.fill(BLACK)

    title = big_font.render(
        "Night Shift Ultimate",
        True,
        WHITE
    )

    screen.blit(title, (300, 100))

    for i, option in enumerate(menu_options):

        color = RED if i == menu_selected else WHITE

        text = font.render(option, True, color)

        screen.blit(text, (500, 300 + i * 60))

# =========================================================
# DRAW OFFICE
# =========================================================

def draw_office():

    screen.blit(office_image, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(40)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))

    controls = font.render(
        "C = Cameras | LEFT/RIGHT = Change Camera | M = Mask",
        True,
        WHITE
    )

    screen.blit(controls, (20, 20))

# =========================================================
# DRAW CAMERA VIEW
# =========================================================

def draw_camera_view(current_room):

    if current_room == "Stage":

        screen.blit(stage_image, (0, 0))

    elif current_room == "Dining":

        screen.blit(dining_image, (0, 0))

    elif current_room == "Hall":

        screen.blit(hall_image, (0, 0))

    elif current_room == "Vent":

        screen.blit(vent_image, (0, 0))

    elif current_room == "Office":

        screen.blit(office_image, (0, 0))

    # =====================================================
    # DARK OVERLAY
    # =====================================================

    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    dark_overlay.set_alpha(90)
    dark_overlay.fill(BLACK)

    screen.blit(dark_overlay, (0, 0))

    # =====================================================
    # STATIC
    # =====================================================

    for i in range(120):

        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        color = random.randint(100, 255)

        pygame.draw.circle(
            screen,
            (color, color, color),
            (x, y),
            1
        )

    # =====================================================
    # VHS LINES
    # =====================================================

    for y in range(0, HEIGHT, 4):

        pygame.draw.line(
            screen,
            (20, 20, 20),
            (0, y),
            (WIDTH, y)
        )

    # =====================================================
    # CAMERA LABEL
    # =====================================================

    cam = big_font.render(
        f"CAMERA: {current_room}",
        True,
        WHITE
    )

    screen.blit(cam, (30, 20))

    # =====================================================
    # SMALL ENEMIES
    # =====================================================

    for enemy in enemies:

        if enemy.room() == current_room:

            x = 580
            y = 350
            size = 16

            pygame.draw.circle(
                screen,
                enemy.color,
                (x, y),
                size
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (x - 5, y - 2),
                3
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (x + 5, y - 2),
                3
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (x - 5, y - 2),
                1
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (x + 5, y - 2),
                1
            )

            warning = font.render(
                f"{enemy.name} DETECTED",
                True,
                enemy.color
            )

            screen.blit(warning, (420, 560))

# =========================================================
# DRAW HUD
# =========================================================

def draw_hud():

    battery_text = font.render(
        f"Battery: {int(battery)}%",
        True,
        GREEN
    )

    screen.blit(battery_text, (920, 20))

    game_hour = min(6, int(night_time // 20))

    if game_hour == 0:
        display = "12 AM"
    else:
        display = f"{game_hour} AM"

    time_text = font.render(
        display,
        True,
        WHITE
    )

    screen.blit(time_text, (920, 60))

    mask_text = font.render(
        "M = MASK",
        True,
        YELLOW
    )

    screen.blit(mask_text, (20, 650))

    # =====================================================
    # MASK OVERLAY
    # =====================================================

    if mask_on:

        mask_overlay = pygame.Surface((WIDTH, HEIGHT))
        mask_overlay.set_alpha(180)
        mask_overlay.fill((40, 40, 40))

        screen.blit(mask_overlay, (0, 0))

        mask_label = big_font.render(
            "MASK ON",
            True,
            WHITE
        )

        screen.blit(mask_label, (470, 320))

    # =====================================================
    # ATTACK WARNING
    # =====================================================

    if attacking_enemy is not None:

        warning = big_font.render(
            f"{attacking_enemy.name} IS ATTACKING",
            True,
            RED
        )

        screen.blit(warning, (250, 120))

        timer_text = font.render(
            f"PUT MASK ON! {attack_timer:.1f}",
            True,
            WHITE
        )

        screen.blit(timer_text, (450, 190))

# =========================================================
# DRAW GAME OVER
# =========================================================

def draw_game_over():

    screen.fill(RED)

    text = big_font.render(
        "JUMPSCARE",
        True,
        WHITE
    )

    screen.blit(text, (430, 250))

    retry = font.render(
        "Press R to Restart",
        True,
        WHITE
    )

    screen.blit(retry, (450, 350))

# =========================================================
# DRAW WIN
# =========================================================

def draw_win():

    screen.fill(BLACK)

    text = big_font.render(
        "6 AM - YOU SURVIVED",
        True,
        GREEN
    )

    screen.blit(text, (230, 250))

    retry = font.render(
        "Press R to Restart",
        True,
        WHITE
    )

    screen.blit(retry, (450, 350))

# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    dt = clock.tick(60) / 1000.0

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # =================================================
            # MENU CONTROLS
            # =================================================

            if state == MENU:

                if event.key == pygame.K_UP:

                    menu_selected = (
                        menu_selected - 1
                    ) % len(menu_options)

                if event.key == pygame.K_DOWN:

                    menu_selected = (
                        menu_selected + 1
                    ) % len(menu_options)

                if event.key == pygame.K_RETURN:

                    if menu_selected == 0:

                        reset_game()
                        state = GAME

                    elif menu_selected == 1:

                        load_game()
                        state = GAME

                    elif menu_selected == 2:

                        running = False

            # =================================================
            # GAME CONTROLS
            # =================================================

            elif state == GAME:

                if event.key == pygame.K_c:
                    camera_open = not camera_open

                if event.key == pygame.K_RIGHT:

                    camera_index = (
                        camera_index + 1
                    ) % len(rooms)

                if event.key == pygame.K_LEFT:

                    camera_index = (
                        camera_index - 1
                    ) % len(rooms)

                if event.key == pygame.K_s:
                    save_game()

                if event.key == pygame.K_m:
                    mask_on = not mask_on

                if event.key == pygame.K_ESCAPE:
                    state = MENU

            # =================================================
            # RESET
            # =================================================

            elif state in [GAME_OVER, WIN]:

                if event.key == pygame.K_r:
                    reset_game()

    # =====================================================
    # MENU
    # =====================================================

    if state == MENU:

        draw_menu()

    # =====================================================
    # GAME
    # =====================================================

    elif state == GAME:

        night_time += dt

        # =================================================
        # BATTERY SYSTEM
        # =================================================

        if camera_open:

            # 1% every 2 seconds
            battery -= 0.5 * dt

        else:

            # 1% every 3 seconds
            battery -= 0.333 * dt

        battery = max(0, battery)

        # =================================================
        # BATTERY DEATH
        # =================================================

        if battery <= 0:
            state = GAME_OVER

        # =================================================
        # ENEMY UPDATES
        # =================================================

        for enemy in enemies:

            enemy.update(dt)

            # attack starts
            if enemy.room() == "Office" and attacking_enemy is None:

                attacking_enemy = enemy

                attack_timer = 2

                camera_open = False

        # =================================================
        # ATTACK LOGIC
        # =================================================

        if attacking_enemy is not None:

            attack_timer -= dt

            # player survives
            if mask_on:

                mask_hold_time += dt

                if mask_hold_time >= 3:

                    attacking_enemy.position = 0

                    attacking_enemy = None

                    attack_timer = 0

                    mask_hold_time = 0

                    mask_on = False

            # player dies
            else:

                if attack_timer <= 0:
                    state = GAME_OVER

        # =================================================
        # DRAWING
        # =================================================

        if not camera_open:

            draw_office()

        else:

            current_room = rooms[camera_index]

            draw_camera_view(current_room)

        draw_hud()

        # =================================================
        # WIN CONDITION
        # =================================================

        if night_time >= 120:
            state = WIN

    # =====================================================
    # GAME OVER
    # =====================================================

    elif state == GAME_OVER:

        draw_game_over()

    # =====================================================
    # WIN
    # =====================================================

    elif state == WIN:

        draw_win()

    pygame.display.flip()

pygame.quit()
sys.exit()








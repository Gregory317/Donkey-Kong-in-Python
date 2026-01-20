import os
import random
import textwrap
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Classic Donkey Kong Rebuild!')
# pygame.display.set_icon('image file')

font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30)

screen = pygame.display.set_mode([window_width, window_height])
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8
EDGE_PADDING = max(4, section_width // 10)  # pixeles extra a cada lado

barrel_spawn_time = 360
barrel_count = barrel_spawn_time / 2
barrel_time = 360
barrel_img = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/barrels/barrel.png'),
                                    (section_width * 1.5, section_height * 2))
flames_img = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/fire.png'),
                                    (section_width * 2, section_height))
barrel_side = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/barrels/barrel2.png'),
                                     (section_width * 2, section_height * 2.5))
dk1 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/dk/dk1.png'),
                             (section_width * 5, section_height * 5))
dk2 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/dk/dk2.png'),
                             (section_width * 5, section_height * 5))
dk3 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/dk/dk3.png'),
                             (section_width * 5, section_height * 5))
peach1 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/peach/peach1.png'),
                                (2 * section_width, 3 * section_height))
peach2 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/peach/peach2.png'),
                                (2 * section_width, 3 * section_height))
fireball = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/fireball.png'),
                                  (1.5 * section_width, 2 * section_height))
fireball2 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/fireball2.png'),
                                   (1.5 * section_width, 2 * section_height))
hammer = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/hammer.png'),
                                   (2 * section_width, 2 * section_height))
standing = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/standing-csm.png'),
                                  (2 * section_width, 2.5 * section_height))
jumping = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/jumping-csm.png'),
                                 (2 * section_width, 2.5 * section_height))
running = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/running-csm.png'),
                                 (2 * section_width, 2.5 * section_height))
climbing1 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/climbing1-csm.png'),
                                   (2 * section_width, 2.5 * section_height))
climbing2 = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/climbing2-csm.png'),
                                   (2 * section_width, 2.5 * section_height))
hammer_stand = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/hammer_stand.png'),
                                      (2.5 * section_width, 2.5 * section_height))
hammer_jump = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/hammer_jump.png'),
                                     (2.5 * section_width, 2.5 * section_height))
hammer_overhead = pygame.transform.scale(pygame.image.load('GameDonkeyKong/PythonDonkeyKong-Main/assets/images/mario/hammer_overhead.png'),
                                         (2.5 * section_width, 3.5 * section_height))

start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope
fireball_trigger = False
active_level = 0
counter = 0
score = 0
high_score = 0
lives = 3
bonus = 6000
first_fireball_trigger = False
victory = False
reset_game = False
levels = [{'bridges': [(1, start_y, 16), (16, start_y - slope, 4),
                       (19, start_y - 2 * slope, 4), (22, start_y - 3 * slope, 4),
                       (25, start_y - 4 * slope, 4), (28, start_y - 5 * slope, 4),
                       (25, row2_y, 4), (22, row2_y - slope, 4),
                       (19, row2_y - 2 * slope, 4), (16, row2_y - 3 * slope, 4),
                       (13, row2_y - 4 * slope, 4), (10, row2_y - 5 * slope, 4),
                       (7, row2_y - 6 * slope, 4), (4, row2_y - 7 * slope, 4),
                       (2, row2_y - 8 * slope, 3), (4, row3_y, 4),
                       (7, row3_y - slope, 4), (10, row3_y - 2 * slope, 4),
                       (13, row3_y - 3 * slope, 4), (16, row3_y - 4 * slope, 4),
                       (19, row3_y - 5 * slope, 4), (22, row3_y - 6 * slope, 4),
                       (25, row3_y - 7 * slope, 4), (28, row3_y - 8 * slope, 3),
                       (25, row4_y, 4), (22, row4_y - slope, 4),
                       (19, row4_y - 2 * slope, 4), (16, row4_y - 3 * slope, 4),
                       (13, row4_y - 4 * slope, 4), (10, row4_y - 5 * slope, 4),
                       (7, row4_y - 6 * slope, 4), (4, row4_y - 7 * slope, 4),
                       (2, row4_y - 8 * slope, 3), (4, row5_y, 4),
                       (7, row5_y - slope, 4), (10, row5_y - 2 * slope, 4),
                       (13, row5_y - 3 * slope, 4), (16, row5_y - 4 * slope, 4),
                       (19, row5_y - 5 * slope, 4), (22, row5_y - 6 * slope, 4),
                       (25, row5_y - 7 * slope, 4), (28, row5_y - 8 * slope, 3),
                       (25, row6_y, 4), (22, row6_y - slope, 4),
                       (19, row6_y - 2 * slope, 4), (16, row6_y - 3 * slope, 4),
                       (2, row6_y - 4 * slope, 15), (13, row6_y - 4 * section_height, 7),
                       (10, row6_y - 3 * section_height, 4)],
           'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                       (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                       (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                       (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                       (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                       (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                       (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                       (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                       (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                       (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
          'hammers': [(4, row6_top + section_height), (4, row4_top+section_height)],
           'target': (13, row6_y - 4 * section_height, 3)}]



# Set up font sizes (you can adjust the size based on your needs)
font_size = 60  # Standard size for options and instructions 
big_font_size = 100  # Bigger font for questions 

# Load fonts
font = pygame.font.Font(None, font_size)  # Default system font with specified size
big_font = pygame.font.Font(None, big_font_size)  # Big font for the question text

# Define color constants (RGB format)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (100, 160, 255) 


def reset():
    global player, barrels, flames, hammers, first_fireball_trigger, victory, lives, bonus
    global barrel_spawn_time, barrel_count, questions_asked, asked_questions, questions_this_life

    questions_this_life = 0
    
    if lives <= 0:
        game_over_screen()
        return
    # Reset the game state
    pygame.time.delay(1000)
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    
    

    # Reset player and state
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    victory = False

def game_over_screen():
    """Displays the Game Over screen with options to restart or quit."""
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER!", 100, window_width // 2, window_height // 2 - 100, RED)
    draw_text(screen, "Press Q to Quit", 50, window_width // 2, window_height // 2, WHITE)
    draw_text(screen, "Press R to Restart", 50, window_width // 2, window_height // 2 + 100, WHITE)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:  # Restart the game
                    reset_game()
                    return


def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0]*section_width, target[1]), (section_width*target[2], 1))
    
    if player.bottom.colliderect(target_rect):
        victory = True
        if not victory:
            game_over()

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Add last line
    return lines


def display_feedback(text, color):
    """Displays feedback text on the screen for 2 seconds."""
    feedback_text = big_font.render(text, True, color)
    feedback_rect = feedback_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.fill(BLACK)  # Clear screen before showing feedback
    screen.blit(feedback_text, feedback_rect)
    pygame.display.flip()

    pygame.time.wait(2000)  # Show for 2 seconds before returning to game
    
def game_over():
    global score
    if lives == 0:
        screen.blit(font.render("Perdiste!", True, 'red'), (window_width // 2, window_height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        reset_game()
    else:
        reset()


def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def splash_screen():
    screen.fill(BLACK)
    draw_text(screen, "Bienvenido a Donkey Kong!", 75, window_width // 2, window_height // 4, GREEN)
    draw_text(screen, "Instrucciones:", 60, window_width // 2, window_height // 4 + 80, LIGHT_BLUE)
    draw_text(screen, "Usa las flechas para moverte.", 50, window_width // 2, window_height // 4 + 140, WHITE)
    draw_text(screen, "Evita los barriles", 50, window_width // 2, window_height // 4 + 190, WHITE)
    draw_text(screen, "Si te golpean, pierdes una vida", 50, window_width // 2, window_height // 4 + 240, WHITE)
    draw_text(screen, "Rescata a la princesa para ganar!", 50, window_width // 2, window_height // 4 + 290, WHITE)
    draw_text(screen, "Presiona cualquier botón para iniciar", 55, window_width // 2, window_height // 4 + 380, GREEN)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def display_victory_screen():
    screen.fill(BLACK)
    draw_text(screen, "VICTORIA!", 100, window_width // 2, window_height // 2 - 50, GREEN)
    draw_text(screen, f"Score: {score}", 60, window_width // 2, window_height // 2 + 50, WHITE)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before continuing the game
    # You can proceed to the next level or end the game
    reset_game  # If you want to reset the game state



##################################################################################################################################################################
class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.hammer = False
        self.max_hammer = 450
        self.hammer_len = self.max_hammer
        self.hammer_pos = 1
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hammer_box = self.rect
        self.rect.center = (x_pos, y_pos)
        self.over_barrel = False
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)

    def update(self):
        self.landed = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1
        if not self.landed and not self.climbing:
            self.y_change += 0.25
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0
        if self.hammer:
            self.hammer_pos = (self.hammer_len // 30) % 2
            self.hammer_len -= 1
            if self.hammer_len == 0:
                self.hammer = False
                self.hammer_len = self.max_hammer

    def draw(self):
        if not self.hammer:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = standing
                else:
                    self.image = running
            if not self.landed and not self.climbing:
                self.image = jumping
            if self.climbing:
                if self.pos == 0:
                    self.image = climbing1
                else:
                    self.image = climbing2
        else:
            if self.hammer_pos == 0:
                self.image = hammer_jump
            else:
                self.image = hammer_overhead
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        self.calc_hitbox()
        if self.hammer_pos == 1 and self.hammer:
            screen.blit(self.image, (self.rect.left, self.rect.top - section_height))
        else:
            screen.blit(self.image, self.rect.topleft)

    def calc_hitbox(self):
        if not self.hammer:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                           (self.rect[2] - 30, self.rect[3] - 10))
        elif self.hammer_pos == 0:
            if self.dir == 1:
                self.hitbox = pygame.rect.Rect((self.rect[0], self.rect[1] + 5),
                                               (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] + self.hitbox[2], self.rect[1] + 5),
                                                   (self.hitbox[2], self.rect[3] - 10))
            else:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 40, self.rect[1] + 5),
                                               (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] - self.hitbox[2], self.rect[1] + 5),
                                                   (self.hitbox[2], self.rect[3] - 10))
        else:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                           (self.rect[2] - 30, self.rect[3] - 10))
            self.hammer_box = pygame.rect.Rect((self.hitbox[0], self.hitbox[1] - section_height),
                                               (self.hitbox[2], section_height))


class Hammer(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.top = y_pos
        self.rect.left = x_pos * section_width
        self.used = False

    def draw(self):
        if not self.used:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
            if self.rect.colliderect(player.hitbox):
                self.kill()
                player.hammer = True
                player.hammer_len = player.max_hammer
                self.used = True


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # opcional: dibujar la forma para debug (comentario)
        # pygame.draw.circle(self.image, (150,75,0), (25,25), 22)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_dir = 1             # dirección persistente: 1 derecha, -1 izquierda
        self.x_speed = 3           # velocidad horizontal
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        # bottom rect ligeramente por encima del borde inferior para evitar penetración en plataformas gruesas
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 2, self.rect.width, 3)
        self.bounce_cooldown = 0   # frames durante los que no se sobrescribe la dirección tras rebotar

    def update(self, fire_trig):
        # gravedad/caída
        if self.y_change < 8 and not self.falling:
            self.y_change += 2

        # detectar plataformas: si bottom colisiona con una plataforma, snap del barril SOBRE la plataforma
        for plat in plats:
            if self.bottom.colliderect(plat):
                # situar el barril encima de la plataforma (evita que quede atascado en su grosor)
                self.rect.bottom = plat.top
                self.y_change = 0
                self.falling = False
                # al apoyarse, no cambiar inmediatamente la dirección; mantenemos x_dir actual
                break

        # colisión con el bidón de aceite (genera fuego)
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    fire_trig = True

        # calcular la dirección preferida según la fila (comportamiento original)
        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                preferred_dir = 1
            else:
                preferred_dir = -1
        else:
            preferred_dir = self.x_dir  # si está cayendo no cambiamos

        # disminuir cooldown si existe
        if self.bounce_cooldown > 0:
            self.bounce_cooldown -= 1

        # sólo sobrescribimos la dirección con la preferida si no acabamos de rebotar
        if self.bounce_cooldown == 0 and not self.falling:
            self.x_dir = preferred_dir

        # mover según dirección persistente y velocidad
        self.rect.move_ip(self.x_dir * self.x_speed, self.y_change)

        # manejo de borde de ventana: si choca con pared, colocarlo dentro y voltear dirección + cooldown
        if self.rect.left <= 0:
            self.rect.left = 0
            self.x_dir = 1
            self.bounce_cooldown = 6
        elif self.rect.right >= window_width:
            self.rect.right = window_width
            self.x_dir = -1
            self.bounce_cooldown = 6

        # fuera de pantalla verticalmente -> eliminar
        if self.rect.top > screen_height:
            self.kill()

        # animación del barril (usa la dirección actual para escoger la animación)
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_dir > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3

        # actualizar "bottom" usado para la detección de plataformas
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 2, self.rect.width, 3)
        return fire_trig

    def check_fall(self):
        already_collided = False
        # área bajo el barril, centrada horizontalmente para detectar escaleras estrechas
        below = pygame.rect.Rect((self.rect.centerx - section_width // 2, self.rect.bottom),
                                 (section_width, section_height))
        for lad in lads:
            if (below.colliderect(lad) or self.rect.colliderect(lad)) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                # probabilidad de caer por escalera (puedes ajustar este número)
                if random.randint(0, 30) == 0:
                    self.falling = True
                    self.y_change = 4
        if not already_collided:
            self.check_lad = False

    def draw(self):
        screen.blit(pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft)


# Añadir función auxiliar para spawnear barriles desde la posición de Donkey Kong
def spawn_barrel_from_kong():
    # Posición donde dibujas a Kong en draw_kong(): x = 3.5 * section_width, y = row6_y - 5.5 * section_height
    kong_x = int(3.5 * section_width)
    kong_y = int(row6_y - 5.5 * section_height)
    # usar el ancho/alto de dk1 (las tres imágenes tienen mismo tamaño) para calcular punto de salida
    spawn_x = kong_x + dk1.get_width() // 2
    # colocar el barril un poco por debajo de DK para que caiga de la plataforma si corresponde
    spawn_y = kong_y + dk1.get_height() - (section_height // 2)
    new_barrel = Barrel(spawn_x, spawn_y)
    barrels.add(new_barrel)

class Flame(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.pos = 1
        self.count = 0
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        self.check_lad = False
        self.climbing = False

    def update(self):
        # CORRECCIÓN: usar self en lugar de la variable global `flame`
        if self.y_change < 3 and not self.climbing:
            self.y_change += 0.25
        for i in range(len(plats)):
            if self.rect.colliderect(plats[i]):
                self.climbing = False
                self.y_change = -4
        # if flame collides with players hitbox - trigger reset of the game (also do this to barrels)
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            self.pos *= -1
            if self.x_count < self.x_max:
                self.x_count += 1
            else:  # row 1,3 and 5 - go further right than left overall, otherwise flip it
                self.x_count = 0
                if self.x_change > 0:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(3, 6)
                    else:
                        self.x_max = random.randint(6, 10)
                else:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(6, 10)
                    else:
                        self.x_max = random.randint(3, 6)
                self.x_change *= -1
        if self.pos == 1:
            if self.x_change > 0:
                self.image = fireball
            else:
                self.image = pygame.transform.flip(fireball, True, False)
        else:
            if self.x_change > 0:
                self.image = fireball2
            else:
                self.image = pygame.transform.flip(fireball2, True, False)
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height or self.rect.top < 0:
            self.kill()

    def check_climb(self):
        already_collided = False
        for lad in lads:
            if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 120) == 120:
                    self.climbing = True
                    self.y_change = - 4
        if not already_collided:
            self.check_lad = False
        if self.rect.bottom < row6_y:
            self.row = 6
        elif self.rect.bottom < row5_y:
            self.row = 5
        elif self.rect.bottom < row4_y:
            self.row = 4
        elif self.rect.bottom < row3_y:
            self.row = 3
        elif self.rect.bottom < row2_y:
            self.row = 2
        else:
            self.row = 1


class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = (225, 51, 129)
        for i in range(self.length):
            bot_coord = self.y_pos + section_height
            left_coord = self.x_pos + (section_width * i)
            mid_coord = left_coord + (section_width * 0.5)
            right_coord = left_coord + section_width
            top_coord = self.y_pos
            # draw 4 lines, top, bot, left diag, right diag
            pygame.draw.line(screen, platform_color, (left_coord, top_coord),
                             (right_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (mid_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (mid_coord, top_coord),
                             (right_coord, bot_coord), line_width)
        # top platform 'surface' usado para colisiones: lo expandimos horizontalmente para eliminar huecos pequeños
        top_line = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        collision_rect = pygame.rect.Rect(top_line.left - EDGE_PADDING, top_line.top,
                                          top_line.width + 2 * EDGE_PADDING, top_line.height)
        return collision_rect


class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(screen, lad_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                (section_width, (lad_height * self.length * section_height + section_height)))
        return body


# function to draw platforms and ladders
def draw_screen():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for ladder in ladders:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)

    return platforms, climbers


def draw_extras():
    # Clear a top bar area for the HUD
    pygame.draw.rect(screen, BLACK, (0, 0, window_width, 100))

    # Display score and high score
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (50, 20))
    screen.blit(high_score_text, (window_width // 2 - high_score_text.get_width() // 2, 20))

    # Display lives and bonus in a properly sized box
    box_width = 400  # Increased box width to fit both labels and values
    box_x = window_width - box_width - 20  # Padding from the right edge
    pygame.draw.rect(screen, WHITE, (box_x, 20, box_width, 60), 2)

    # Lives: half white and half green
    lives_text = font2.render("Lives:", True, WHITE)
    lives_value = font2.render(f"{lives}", True, GREEN)
    screen.blit(lives_text, (box_x + 0, 30))
    screen.blit(lives_value, (box_x + 100, 30))  # Increased the gap to avoid overlap

    # Bonus: half white and half green
    bonus_text = font2.render("Bonus:", True, WHITE)
    bonus_value = font2.render(f"{bonus}", True, GREEN)
    screen.blit(bonus_text, (box_x + 170, 30))  # Adjusted for spacing
    screen.blit(bonus_value, (box_x + 300, 30))  # Moved slightly to the right

    # Draw Peach sprite based on game state
    peach_position = (10 * section_width, row6_y - 6 * section_height)
    if barrel_count < barrel_spawn_time / 2:
        screen.blit(peach1, peach_position)
    else:
        screen.blit(peach2, peach_position)

    # Draw oil drum, stationary barrels, and Donkey Kong
    oil = draw_oil()
    draw_barrels()
    draw_kong()

    return oil



def draw_oil():
    x_coord, y_coord = 4 * section_width, window_height - 4.5 * section_height
    oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2 * section_width, 2.5 * section_height])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 * section_width, y_coord, 2.2 * section_width, .2 * section_height])
    pygame.draw.rect(screen, 'blue',
                     [x_coord - 0.1 * section_width, y_coord + 2.3 * section_height, 2.2 * section_width,
                      .2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord + 0.1 * section_width, y_coord + .2 * section_height, .2 * section_width,
                      2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 0.5 * section_height, 2 * section_width, .2 * section_height])

    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 1.7 * section_height, 2 * section_width, .2 * section_height])
    screen.blit(font2.render('OIL', True, 'light blue'), (x_coord + .4 * section_width, y_coord + 0.7 * section_height))
    for i in range(4):
        pygame.draw.circle(screen, 'red',
                           (x_coord + 0.5 * section_width + i * 0.4 * section_width, y_coord + 2.1 * section_height), 3)
    # draw the flames on top
    if counter < 15 or 30 < counter < 45:
        screen.blit(flames_img, (x_coord, y_coord - section_height))
    else:
        screen.blit(pygame.transform.flip(flames_img, True, False), (x_coord, y_coord - section_height))
    return oil


def draw_barrels():
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 5.4 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 5.4 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 7.7 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 7.7 * section_height))


def draw_kong():
    phase_time = barrel_time // 4
    if barrel_spawn_time - barrel_count > 3 * phase_time:
        dk_img = dk2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        dk_img = dk1
    elif barrel_spawn_time - barrel_count > phase_time:
        dk_img = dk3
    else:
        dk_img = pygame.transform.flip(dk1, True, False)
        screen.blit(barrel_img, (250, 250))
    screen.blit(dk_img, (3.5 * section_width, row6_y - 5.5 * section_height))


def check_climb():
    can_climb = False
    climb_down = False
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or player.y_change < 0)) or \
            (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False
    return can_climb, climb_down


def barrel_collide(reset):
    global score
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl):
            player.over_barrel = True
            score += 100
    if player.landed:
        player.over_barrel = False

    return reset


def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0] * section_width, target[1]), (section_width * target[2], 1))
    
    if player.bottom.colliderect(target_rect):
        victory = True
        # Trigger victory screen and handle the end of the level
        display_victory_screen()
        return True
    return False



barrels = pygame.sprite.Group()
flames = pygame.sprite.Group()
hammers = pygame.sprite.Group()
hammers_list = levels[active_level]['hammers']
for ham in hammers_list:
    hammers.add(Hammer(*ham))
player = Player(250, window_height - 130)




splash_screen()

run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if counter < 60:
        counter += 1
    else:
        counter = 0
        if bonus > 0:
            bonus -= 100

    # draw platforms and ladders on the screen in dedicated function
    plats, lads = draw_screen()
    oil_drum = draw_extras()
    climb, down = check_climb()
    victory = check_victory()
    if barrel_count < barrel_spawn_time:
        barrel_count += 1
    else:
        barrel_count = random.randint(0, 120)
        barrel_time = barrel_spawn_time - barrel_count
        # crear barril lanzado por Donkey Kong en su plataforma
        spawn_barrel_from_kong()
        if not first_fireball_trigger:
            flame = Flame(5*section_width, window_height - 4*section_height)
            flames.add(flame)
            first_fireball_trigger = True
    for barrel in barrels:
        barrel.draw()
        barrel.check_fall()
        fireball_trigger = barrel.update(fireball_trigger)
        if barrel.rect.colliderect(player.hammer_box) and player.hammer:
            barrel.kill()
            score += 500

    if fireball_trigger:
        flame = Flame(5 * section_width, window_height - 4 * section_height)
        flames.add(flame)
        fireball_trigger = False

    for flame in flames:
        flame.check_climb()
        if flame.rect.colliderect(player.hitbox):
            reset_game = True
    flames.draw(screen)
    flames.update()
    player.update()
    player.draw()
    for ham in hammers:
        ham.draw()

    reset_game = barrel_collide(reset_game)
    if reset_game:
        if lives > 0:
            reset()
            reset_game = False
        else:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not player.climbing:
                player.x_change = 1
                player.dir = 1
            if event.key == pygame.K_LEFT and not player.climbing:
                player.x_change = -1
                player.dir = -1
            if event.key == pygame.K_SPACE and player.landed:
                player.landed = False
                player.y_change = -6
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = -2
                    player.x_change = 0
                    player.climbing = True
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 2
                    player.x_change = 0
                    player.climbing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_LEFT:
                player.x_change = 0
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
            if event.key == pygame.K_DOWN:
                if climb:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
    if victory:
        screen.blit(font.render('VICTORY!', True, 'white'), (window_width/2, window_height/2))
        reset_game = True
        # active_level += 1
        lives += 1
        score += bonus
        if score > high_score:
            high_score = score
        score = 0
        player.climbing = False

    pygame.display.flip()
pygame.quit()
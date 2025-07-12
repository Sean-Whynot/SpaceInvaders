import pygame
import math
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
width = 1920
height = 1080

# Create the screen
screen = pygame.display.set_mode((width, height))

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load('images/background.png')

# Player
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('images/player.png'), (128, 128))
        self.x = x
        self.y = y
        self.x_change = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player = Player(900, 800)

# Alien
class Alien:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('images/alien.png'), (128, 128))
        self.x = x
        self.y = y
        self.x_change = 0.125
        self.last_shot_time = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

aliens = []
level = 1
# Alien
# Alien Bullet
class AlienBullet:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('images/alien_bullet.png'), (64, 64))
        self.x = x
        self.y = y
        self.y_change = 4

    def draw(self):
        screen.blit(self.image, (self.x + 32, self.y + 20))

class Pinky(Alien):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(pygame.image.load('images/pinky.png'), (128, 128))
        self.x_change = 0.25  # Faster than the original alien

    def shoot_triple(self):
        # Shoots three bullets in different directions
        directions = [0, 45, -45]  # Straight, 45 degrees right, 45 degrees left
        for angle in directions:
            alien_bullets.append(RoundBullet(self.x, self.y, angle))

class RoundBullet(AlienBullet):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y)
        self.image = pygame.transform.scale(pygame.image.load('images/round_bullet.png'), (64, 64))
        self.angle = math.radians(angle)  # Convert angle to radians
        self.speed = 4

    def update(self):
        # Move the bullet based on the angle
        self.x += self.speed * math.sin(self.angle)
        self.y += self.speed * math.cos(self.angle)

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('images/player_bullet.png'), (64, 64))
        self.x = x
        self.y = y
        self.y_change = -10

    def draw(self):
        screen.blit(self.image, (self.x + 32, self.y + 20))

    def update(self):
        self.y += self.y_change


def isCollision(obj1X, obj1Y, obj2X, obj2Y):
    distance = math.sqrt(math.pow(obj1X - obj2X, 2) + (math.pow(obj1Y - obj2Y, 2)))
    if distance < 64:
        return True
    else:
        return False

bullets = []
alien_bullets = []
last_shot_time = 0
shoot_delay = 100  # milliseconds

# Sound effects
laser_sound = pygame.mixer.Sound('sounds/laser.wav')
explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.play(-1)

initial_alien_count = 32 # 4 rows * 8 columns

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Score
score = 0
font = pygame.font.Font(None, 32)

def show_score(x, y):
    score_text = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

# Lives
lives = 3
live_image = pygame.image.load('images/live.png')

def show_lives(x, y):
    for i in range(lives):
        screen.blit(live_image, (x + i * 30, y))

# Game Over / Win flags
game_over = False
game_won = False

# Game States
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
current_state = STATE_TITLE

# Game Reset Function
def reset_game():
    global player, aliens, bullets, alien_bullets, score, lives, game_over, game_won, current_state, high_score, level, last_shot_time
    player = Player(900, 800)
    aliens = []
    bullets = []
    alien_bullets = []
    score = 0
    lives = 3
    game_over = False
    game_won = False
    high_score = load_highscore()
    level = 1
    last_shot_time = 0
    spawn_level_aliens()
    current_state = STATE_PLAYING

def respawn_aliens():
    global aliens, level
    level += 1
    spawn_level_aliens()

def spawn_level_aliens():
    global aliens
    aliens = []
    if level == 1:
        for i in range(1):
            for j in range(8):
                aliens.append(Alien(j * 160 + 176, i * 100 + 100))
    else:
        for i in range(5):
            aliens.append(Alien(i * 160 + 176, 100))
        for i in range(5):
            aliens.append(Pinky(i * 160 + 176, 300))

running = True
while running:
    if current_state == STATE_TITLE:
        screen.blit(background, (0, 0))
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("Space Invaders", True, (255, 255, 255))
        screen.blit(title_text, (width / 2 - title_text.get_width() / 2, height / 4))

        highscore_text = font.render("High Score: " + str(load_highscore()), True, (255, 255, 255))
        screen.blit(highscore_text, (width / 2 - highscore_text.get_width() / 2, height / 4 + 70))

        instructions_font = pygame.font.Font(None, 32)
        instructions_text = instructions_font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(instructions_text, (width / 2 - instructions_text.get_width() / 2, height / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()

        pygame.display.update()

    elif current_state == STATE_PLAYING:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -5
                if event.key == pygame.K_RIGHT:
                    player.x_change = 5
                if event.key == pygame.K_SPACE:
                    if current_time - last_shot_time > shoot_delay:
                        laser_sound.play()
                        bullets.append(Bullet(player.x, player.y))
                        last_shot_time = current_time
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
        
        player.x += player.x_change
        if player.x <= 0:
            player.x = 0
        elif player.x >= 1792:
            player.x = 1792

        # Alien Movement
        for alien in aliens:
            alien.x += alien.x_change

        move_down = False
        for alien in aliens:
            if alien.x <= 0 or alien.x >= 1792:
                move_down = True
        
        if move_down:
            for alien in aliens:
                alien.x_change *= -1
                alien.y += 40

        # Alien Shooting
        for alien in aliens:
            # Adjust shooting frequency based on remaining aliens
            # The fewer aliens, the higher the chance of shooting
            # shooting_chance_max = max(100, int(8000 * (len(aliens) / initial_alien_count) / (1 + (level - 1) * 0.5)))
            # if random.randint(0, shooting_chance_max) == 1:
            if isinstance(alien, Pinky):
                if current_time - alien.last_shot_time > 1000: # 1 second
                    if random.random() < 0.1: # 10% chance
                        laser_sound.play()
                        alien.shoot_triple()
                    alien.last_shot_time = current_time
            else:
                # Check if player is directly below the alien
                if player.x < alien.x + alien.image.get_width() and player.x + player.image.get_width() > alien.x:
                    if current_time - alien.last_shot_time > 1000: # 1 second
                        if random.random() < 0.1: # 10% chance
                            laser_sound.play()
                            alien_bullets.append(AlienBullet(alien.x, alien.y))
                        alien.last_shot_time = current_time

        # Bullet Movement
        for bullet in bullets:
            bullet.update()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Alien Bullet Movement
        for alien_bullet in alien_bullets:
            if isinstance(alien_bullet, RoundBullet):
                alien_bullet.update()
            else:
                alien_bullet.y += alien_bullet.y_change
            if alien_bullet.y > height:
                alien_bullets.remove(alien_bullet)

        # Collision
        for bullet in bullets:
            for alien in aliens:
                collision = isCollision(alien.x, alien.y, bullet.x, bullet.y)
                if collision:
                    explosion_sound.play()
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    if isinstance(alien, Pinky):
                        score += 100
                    else:
                        score += 50
                    break

        # Player Collision
        for alien_bullet in alien_bullets:
            collision = isCollision(player.x, player.y, alien_bullet.x, alien_bullet.y)
            if collision:
                lives -= 1
                alien_bullets.remove(alien_bullet)
                if lives <= 0:
                    explosion_sound.play()
                    game_over = True

        # Alien reaches bottom
        for alien in aliens:
            if alien.y >= 450:
                game_over = True
                break

        # Win condition
        if not aliens:
            respawn_aliens()

        if game_over:
            if score > high_score:
                save_highscore(score)
            current_state = STATE_GAME_OVER

        screen.blit(background, (0, 0))
        player.draw()

        for alien in aliens:
            alien.draw()
        
        for bullet in bullets:
            bullet.draw()

        for alien_bullet in alien_bullets:
            alien_bullet.draw()

        show_score(width - 150, 10)
        show_lives(10, 10)

        pygame.display.update()

    elif current_state == STATE_GAME_OVER:
        screen.blit(background, (0, 0))
        if game_won:
            message = "YOU WIN!"
        else:
            message = "GAME OVER"

        game_over_font = pygame.font.Font(None, 64)
        game_over_text = game_over_font.render(message, True, (255, 255, 255))
        screen.blit(game_over_text, (width / 2 - game_over_text.get_width() / 2, height / 2 - game_over_text.get_height() / 2 - 50))

        final_score_text = font.render("Final Score: " + str(score), True, (255, 255, 255))
        screen.blit(final_score_text, (width / 2 - final_score_text.get_width() / 2, height / 2 - game_over_text.get_height() / 2))

        highscore_text = font.render("High Score: " + str(load_highscore()), True, (255, 255, 255))
        screen.blit(highscore_text, (width / 2 - highscore_text.get_width() / 2, height / 2 - game_over_text.get_height() / 2 + 30))

        play_again_font = pygame.font.Font(None, 32)
        play_again_text = play_again_font.render("Press R to Play Again", True, (255, 255, 255))
        screen.blit(play_again_text, (width / 2 - play_again_text.get_width() / 2, height / 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        pygame.display.update()

pygame.quit()

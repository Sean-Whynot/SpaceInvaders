import pygame
import math
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
width = 800
height = 600

# Create the screen
screen = pygame.display.set_mode((width, height))

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load('images/background.png')

# Player
class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/player.png')
        self.x = x
        self.y = y
        self.x_change = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player = Player(370, 480)

# Alien
class Alien:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/alien.png')
        self.x = x
        self.y = y
        self.x_change = 0.125

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

aliens = []
for i in range(4):
    for j in range(8):
        aliens.append(Alien(j * 80 + 88, i * 50 + 50))

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/player_bullet.png')
        self.x = x
        self.y = y
        self.y_change = -10
        self.state = "ready" # "ready" - you can't see the bullet, "fire" - the bullet is moving

    def draw(self):
        if self.state == "fire":
            screen.blit(self.image, (self.x + 16, self.y + 10))

# Alien Bullet
class AlienBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/alien_bullet.png')
        self.x = x
        self.y = y
        self.y_change = 5

    def draw(self):
        screen.blit(self.image, (self.x + 16, self.y + 10))

def isCollision(obj1X, obj1Y, obj2X, obj2Y):
    distance = math.sqrt(math.pow(obj1X - obj2X, 2) + (math.pow(obj1Y - obj2Y, 2)))
    if distance < 27:
        return True
    else:
        return False

bullet = Bullet(0, 480)
alien_bullets = []

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
    global player, aliens, bullet, alien_bullets, score, lives, game_over, game_won, current_state, high_score, level
    player = Player(370, 480)
    aliens = []
    for i in range(4):
        for j in range(8):
            aliens.append(Alien(j * 80 + 88, i * 50 + 50))
    bullet = Bullet(0, 480)
    alien_bullets = []
    score = 0
    lives = 3
    game_over = False
    game_won = False
    high_score = load_highscore()
    level = 1
    current_state = STATE_PLAYING

def respawn_aliens():
    global aliens, level
    aliens = []
    for i in range(4):
        for j in range(8):
            aliens.append(Alien(j * 80 + 88, i * 50 + 50))
    level += 1

# Game loop
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
                    if bullet.state == "ready":
                        laser_sound.play()
                        bullet.x = player.x
                        bullet.state = "fire"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
        
        player.x += player.x_change
        if player.x <= 0:
            player.x = 0
        elif player.x >= 736:
            player.x = 736

        # Alien Movement
        for alien in aliens:
            alien.x += alien.x_change * (1 + (level - 1) * 0.5)

        move_down = False
        for alien in aliens:
            if alien.x <= 0 or alien.x >= 736:
                move_down = True
        
        if move_down:
            for alien in aliens:
                alien.x_change *= -1
                alien.y += 40

        # Alien Shooting
        for alien in aliens:
            # Adjust shooting frequency based on remaining aliens
            # The fewer aliens, the higher the chance of shooting
            shooting_chance_max = max(100, int(8000 * (len(aliens) / initial_alien_count) / (1 + (level - 1) * 0.5)))
            if random.randint(0, shooting_chance_max) == 1:
                laser_sound.play()
                alien_bullets.append(AlienBullet(alien.x, alien.y))

        # Bullet Movement
        if bullet.y <= 0:
            bullet.y = 480
            bullet.state = "ready"

        if bullet.state == "fire":
            bullet.y += bullet.y_change

        # Alien Bullet Movement
        for alien_bullet in alien_bullets:
            alien_bullet.y += alien_bullet.y_change
            if alien_bullet.y > 600:
                alien_bullets.remove(alien_bullet)

        # Collision
        for alien in aliens:
            collision = isCollision(alien.x, alien.y, bullet.x, bullet.y)
            if collision and bullet.state == "fire":
                explosion_sound.play()
                bullet.y = 480
                bullet.state = "ready"
                aliens.remove(alien)
                score += 50

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

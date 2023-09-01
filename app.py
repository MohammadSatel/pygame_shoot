import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (20, 0, 30)  # Purple-Black
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
ENEMY_SCORE = 25

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Shooting Game")

# Load images
player_image = pygame.image.load("player.png")
bullet_image = pygame.image.load("bullet.png")
enemy_image = pygame.image.load("enemy.png")

# Create player
player_rect = player_image.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.centery = SCREEN_HEIGHT - 50

# Create bullets
bullets = []

# Create enemies
enemies = []

# Create a score variable
score = 0

font = pygame.font.Font(None, 36)

def spawn_enemy():
    enemy_rect = enemy_image.get_rect()
    enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
    enemy_rect.y = 0
    enemies.append(enemy_rect)

# Game loop
running = True
clock = pygame.time.Clock()
shooting = False  # Indicates if the spacebar is being held down

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Shooting
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shooting = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            shooting = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += PLAYER_SPEED

    # Shooting
    if shooting:
        bullet_rect = bullet_image.get_rect()
        bullet_rect.centerx = player_rect.centerx
        bullet_rect.centery = player_rect.centery
        bullets.append(bullet_rect)

    # Bullet movement
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Enemy movement and collision
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
        if enemy.colliderect(player_rect):
            running = False
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Spawn new enemies
    if random.randint(0, 100) < 2:
        spawn_enemy()

    # Bullet and enemy collision
    bullets_to_remove = []
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets_to_remove.append(bullet)
                enemies.remove(enemy)
                score += ENEMY_SCORE
                break
    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    # Clear the screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Draw player
    screen.blit(player_image, player_rect)

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

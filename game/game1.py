import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
CYAN = (0,255,255)
GREEN = (0, 73, 83)
YELLOW = (255,255,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREY = (150, 150, 150)
RADIUS = 10
USER_RADIUS = 8
BULLET_COUNT = 2
GREY_CIRCLE_RADIUS = 5  

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Game")

# Circle objects
middle_circle = pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), RADIUS)
user_circle = pygame.draw.circle(screen, GREEN, (WIDTH // 2, HEIGHT // 2), USER_RADIUS)

# Game variables
user_x, user_y = WIDTH // 2, HEIGHT // 2
projectiles = []
last_shot_time = 0
score_home = 0
score_away = 0
font = pygame.font.Font(None, 36)

# Grey circles
grey_circles = []
grey_circle_spawn_time = 0
grey_circle_duration = 1.5
grey_circle_spawn_interval = 2

# Calculate the initial angle
def calculate_initial_angle(user_x, user_y):
    angle = math.atan2(user_y - HEIGHT // 2, user_x - WIDTH // 2)
    return angle

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for grey_circle in grey_circles:
                if grey_circle.colliderect(pygame.Rect(event.pos[0] - GREY_CIRCLE_RADIUS, event.pos[1] - GREY_CIRCLE_RADIUS, GREY_CIRCLE_RADIUS * 2, GREY_CIRCLE_RADIUS * 2)):
                    grey_circles.remove(grey_circle)
                    score_home += 0.10

    # Get the mouse position
    user_x, user_y = pygame.mouse.get_pos()
    user_circle.center = (user_x, user_y)

    # Spawn grey circles every 2 seconds
    current_time = time.time()
    if current_time - grey_circle_spawn_time >= grey_circle_spawn_interval:
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        grey_circles.append(pygame.Rect(x - GREY_CIRCLE_RADIUS, y - GREY_CIRCLE_RADIUS, GREY_CIRCLE_RADIUS * 2, GREY_CIRCLE_RADIUS * 2))
        grey_circle_spawn_time = current_time

    # Remove expired grey circles
    grey_circles = [circle for circle in grey_circles if current_time - grey_circle_spawn_time <= grey_circle_duration]

    # Shooting projectiles
    if current_time - last_shot_time >= 1:
        for _ in range(BULLET_COUNT):
            initial_angle = calculate_initial_angle(user_x, user_y)
            scatter = math.radians(random.uniform(-10, 10))
            angle = initial_angle + scatter
            projectile_x = WIDTH // 2 + RADIUS * math.cos(angle)
            projectile_y = HEIGHT // 2 + RADIUS * math.sin(angle)
            projectiles.append((projectile_x, projectile_y, angle))
        last_shot_time = current_time

    # Update and draw projectiles
    new_projectiles = []
    for projectile in projectiles:
        x, y, angle = projectile
        speed = 1
        x += speed * math.cos(angle)
        y += speed * math.sin(angle)
        pygame.draw.circle(screen, GREY, (int(x), int(y)), 5)
    
        if not user_circle.collidepoint(x, y):
            new_projectiles.append((x, y, angle))
        else:
            score_away += 0.50
            
    projectiles = new_projectiles

    # Draw circle objects
    pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), RADIUS)
    pygame.draw.circle(screen, GREEN, (user_x, user_y), USER_RADIUS)

    # Draw grey circles
    for circle in grey_circles:
        pygame.draw.circle(screen, YELLOW, (circle.center[0], circle.center[1]), GREY_CIRCLE_RADIUS)

    # Display the score
    home_score_text = font.render("Home: " + str(int(score_home)), True, CYAN)
    away_score_text = font.render("Away: " + str(int(score_away)), True, RED)
    screen.blit(home_score_text, (20, 20))
    screen.blit(away_score_text, (20, 60))

    pygame.display.update()


pygame.quit()
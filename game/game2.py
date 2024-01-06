import pygame
import math
import random
import time

pygame.init()
nameStr="cthulhu-34354"
GAME_TIME = 180
middle_circle_image = pygame.image.load(nameStr+".png")

DENOMINATOR = GAME_TIME / 6
CLUTCH = GAME_TIME / 4

islifeRegen = False
enemyManpower=20

Int=int(nameStr[-5])
Tec=int(nameStr[-4])
Off=int(nameStr[-3])
Spd=int(nameStr[-2])
Def=int(nameStr[-1])

print(Int)
print(Tec)
print(Off)
print(Spd)
print(Def)

IN=[300, 275, 250, 225, 200, 175]
TQ=[1, 0.9, 0.8, 0.7, 0.6, 0.5]
OF=[10, 15, 20, 25, 30, 35]
SP=[3, 4, 5, 6, 7, 8]
DF=[5, 6, 7, 8, 9, 10] 

# Constants
WIDTH, HEIGHT = 600, 400
CYAN = (0, 255, 255)
GREEN = (0, 73, 83)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (150, 150, 150)
RADIUS = 10
USER_RADIUS = 10

grey_circle_duration = 1               
grey_circle_spawn_interval = 1 
HIT_LINE = IN[Int-1]
BULLET_RATE = TQ[Tec-1]                         
OFFENSE = OF[Off-1]                            
BULLET_SPEED = SP[Spd-1]                     
BULLET_COUNT = DF[Def-1]                    


GREY_CIRCLE_RADIUS = 5

TIMER_FONT = pygame.font.Font(None, 36)
TIMER_COLOR = CYAN

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Game")

# user circle 
user_circle = pygame.draw.circle(screen, GREEN, (WIDTH // 2, HEIGHT // 2), USER_RADIUS)

# Game variables
user_x, user_y = WIDTH // 2, HEIGHT // 2
projectiles = []
last_shot_time = time.time()
score_home = 0
score_away = 0
font = pygame.font.Font(None, 36)
last_hit=0
count=0
isClutch = False


# grey circles
grey_circles = []
grey_circle_spawn_time = 0


# Flag to control bullet firing
fire_bullets = False
isGameEnded = False

# Calculate the initial angle
def calculate_initial_angle(user_x, user_y):
    angle = math.atan2(user_y - 70, user_x - WIDTH // 2)
    return angle


running = True
clock = pygame.time.Clock()
last_frame_time = pygame.time.get_ticks()  # Initialize last_frame_time

score_away_last_increment_time = pygame.time.get_ticks()

# Game loop
while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - last_frame_time
    last_frame_time = current_time  # Update last_frame_time
    
    #Draw Images
    middle_circle_rect = middle_circle_image.get_rect()
    middle_circle_rect.center = (WIDTH // 2, 70)
    screen.blit(middle_circle_image, middle_circle_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for grey_circle in grey_circles:
                if grey_circle.colliderect(pygame.Rect(event.pos[0] - GREY_CIRCLE_RADIUS, event.pos[1] - GREY_CIRCLE_RADIUS, GREY_CIRCLE_RADIUS * 2, GREY_CIRCLE_RADIUS * 2)):
                    grey_circles.remove(grey_circle)
                    if fire_bullets:
                        if not isGameEnded:
                            if isClutch:
                                score_home += 2
                            else:
                                score_home += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                fire_bullets = not fire_bullets  # Toggle the bullet firing flag
        
    # Get the mouse position
    user_x, user_y = pygame.mouse.get_pos()
    user_circle.center = (user_x, user_y)

    # Spawn grey circles every 2 seconds
    current_time = time.time()
    last_frame_time = time.time()
    elapsed_time = current_time - last_frame_time
    last_frame_time = current_time  # Update last_frame_time
    
    if current_time - grey_circle_spawn_time >= grey_circle_spawn_interval and fire_bullets: 
        x = random.randint(50, WIDTH - 50)
        y = random.randint(120, HIT_LINE)#HEIGHT // 2
        grey_circles.append(pygame.Rect(x - GREY_CIRCLE_RADIUS, y - GREY_CIRCLE_RADIUS, GREY_CIRCLE_RADIUS * 2, GREY_CIRCLE_RADIUS * 2))
        grey_circle_spawn_time = current_time

    # Remove expired grey circles
    grey_circles = [circle for circle in grey_circles if current_time - grey_circle_spawn_time <= grey_circle_duration]

    # Handle shooting projectiles if the flag allows
    if fire_bullets and not isGameEnded and current_time - last_shot_time >= BULLET_RATE:
        for _ in range(BULLET_COUNT):
            count = count+1
            initial_angle = calculate_initial_angle(user_x, user_y)
            scatter = math.radians(random.uniform(-60, 60))
            angle = initial_angle + scatter
            projectile_x = WIDTH // 2 + RADIUS * math.cos(angle)
            projectile_y = 70 + RADIUS * math.sin(angle)
            projectiles.append((projectile_x, projectile_y, angle))
        last_shot_time = current_time


    time_left=GAME_TIME - (count*BULLET_RATE/BULLET_COUNT)     
    
    
    # Update and draw projectiles
    new_projectiles = []
    for projectile in projectiles:
        x, y, angle = projectile
        #scatter_speed = math.radians(random.uniform(-0.5, 0.5))

        x += BULLET_SPEED * math.cos(angle) 
        y += BULLET_SPEED * math.sin(angle) 
        pygame.draw.circle(screen, GREY, (int(x), int(y)), 5)

        if not user_circle.collidepoint(x, y):
            new_projectiles.append((x, y, angle))
        else:
            # Check if 0.2 seconds have passed since the last increment
            current_time = pygame.time.get_ticks()
            if current_time - score_away_last_increment_time >= 200:
                if not isGameEnded:
                    score_amount = random.uniform(1, OFFENSE)
                    score_away += score_amount #15
                    score_away_last_increment_time = current_time  # Update the last increment time
                    if islifeRegen:
                        last_hit=time_left
                        print(last_hit)
    
    if time_left <= CLUTCH and not isClutch and score_away < score_home:
        isClutch = True
        BULLET_SPEED +=1
        print(BULLET_SPEED)
        
    
    if (time_left-last_hit) > 5 and islifeRegen:
        if score_away > 0:
            score_away = score_away-1
            last_hit=time_left
            print(last_hit)
        
    projectiles = new_projectiles

    # Draw the circle objects
    pygame.draw.circle(screen, GREEN, (user_x, user_y), USER_RADIUS)

    # Draw the yellow circles
    if fire_bullets and not isGameEnded:
        for circle in grey_circles:
            pygame.draw.circle(screen, YELLOW, (circle.center[0], circle.center[1]), GREY_CIRCLE_RADIUS)

    # Display the score
    home_score_text = font.render("Home: " + str(int(score_home))+" : "+str(int(score_home/DENOMINATOR)), True, CYAN)
    away_score_text = font.render("Away: " + str(int(score_away))+" : "+str(int(score_away/DENOMINATOR)), True, RED)
    screen.blit(home_score_text, (10, 10))
    screen.blit(away_score_text, (10, 40))
    

    
    
    if time_left <= 0 or (islifeRegen and score_away >= 10):
        time_left = 0 
        timer_text2 = TIMER_FONT.render(f"Game Ended", True, GREY)
        home_score_end = font.render(str(int(score_home/DENOMINATOR)) + "  -", True, CYAN)
        away_score_end = font.render(str(int(score_away/DENOMINATOR)), True, RED)
        screen.blit(timer_text2, (WIDTH - 150, 50))
        screen.blit(home_score_end, (WIDTH - 100, 80))
        screen.blit(away_score_end, (WIDTH - 50, 80))
        isGameEnded = True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            count=0
            score_away=0
            score_home=0
            isGameEnded=False
            fire_bullets = True
            grey_circles = []
            last_hit=0
            if isClutch:
                BULLET_SPEED -=1
                isClutch = False
            
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        count=0
        score_away=0
        score_home=0
        isGameEnded=False
        fire_bullets = True
        grey_circles = []
        last_hit=0
        if isClutch:
            BULLET_SPEED -=1
            isClutch = False
    
    
        
    # Draw the game timer
    timer_text = TIMER_FONT.render(""+str(int(time_left)), True, WHITE)
    screen.blit(timer_text, (WIDTH - 50, 20))
    
    
    pygame.display.update()
    # Limit the frame rate
    clock.tick(60) 



pygame.quit()
import pygame
import random
import math
from pygame import mixer

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Personalización
pygame.display.set_caption("ESP Warriors")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('assets/images/background.jpg')
mixer.music.load('assets/sounds/background.wav')
mixer.music.play(-1)

# Definir fuentes
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
instructions_font = pygame.font.Font('freesansbold.ttf', 28)

# Monstruos
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
num_of_monsters = 6
for i in range(num_of_monsters):
    monsterImg.append(pygame.image.load('assets/images/monster.png'))
    monsterX.append(random.randint(30, 60))
    monsterY.append(random.randint(0, 600))
    monsterY_change.append(0.5)
    monsterX_change.append(40)

# Balas
bulletImg = pygame.image.load('assets/images/bullet.png')
bulletX = 600
bulletY = 250
bulletX_change = 1
bullet_state = "ready"

# Soldado
soldierImg = pygame.image.load('assets/images/soldier.png')
soldierX = 600
soldierY = 250
soldierY_change = 0

# Puntuación
score_value = 0
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))

def soldier(x, y):
    screen.blit(soldierImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt(math.pow(monsterX - bulletX, 2) + math.pow(monsterY - bulletY, 2))
    return distance < 27

# Función para mostrar las instrucciones
def show_instructions():
    instructions_running = True
    while instructions_running:
        screen.fill((0, 0, 0))
        instructions_title = over_font.render("Cómo Jugar", True, (255, 255, 255))
        instructions_text = instructions_font.render("Debes matar a los monstruos,", True, (255, 255, 255))
        instructions_text2 = instructions_font.render("Usa las flechas y spacebar", True, (255, 255, 255))
        return_text = font.render("Preiona la b para volver", True, (255, 255, 255))
        screen.blit(instructions_title, (200, 100))
        screen.blit(instructions_text, (150, 250))
        screen.blit(instructions_text2, (120, 300))
        screen.blit(return_text, (150, 500))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions_running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Regresar al menú principal
                    instructions_running = False

        pygame.display.update()

# Función de menú
def show_menu():
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))
        title = over_font.render("ESP Warriors", True, (255, 255, 255))
        play_button = font.render("Presiona enter para jugar", True, (255, 255, 255))
        instructions_button = font.render("Presiona I para ver las instrucciones", True, (255, 255, 255))
        quit_button = font.render("Presiona Esc para salir :(", True, (255, 255, 255))
        screen.blit(title, (200, 150))
        screen.blit(play_button, (200, 300))
        screen.blit(instructions_button, (200, 350))
        screen.blit(quit_button, (200, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter para iniciar el juego
                    menu_running = False
                if event.key == pygame.K_i:  # Tecla "I" para mostrar las instrucciones
                    show_instructions()
                if event.key == pygame.K_ESCAPE:  # Esc para salir
                    pygame.quit()
                    quit()
                
        
        pygame.display.update()

# Ciclo principal del juego
running = True
show_menu()  # Mostrar el menú al inicio
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movimientos desde el teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                soldierY_change = -1
            if event.key == pygame.K_DOWN:
                soldierY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('assets/sounds/bullet-sound.wav')
                    bullet_Sound.play()
                    bulletY = soldierY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                soldierY_change = 0

    soldierY += soldierY_change
    if soldierY <= 0:
        soldierY = 0
    elif soldierY >= 536:
        soldierY = 536

    # Monstruos
    for i in range(num_of_monsters):
        if monsterX[i] > 600:
            for j in range(num_of_monsters):
                monsterX[j] = 2000
            game_over_text()
            break

        monsterY[i] += monsterY_change[i]
        if monsterY[i] <= 0:
            monsterY_change[i] = 0.5
            monsterX[i] += monsterX_change[i]
        elif monsterY[i] >= 536:
            monsterY_change[i] = -0.5
            monsterX[i] += monsterX_change[i]

        # Colisión
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('assets/sounds/explosion.wav')
            explosion_Sound.play()
            bulletX = 600
            bullet_state = "ready"
            score_value += 1
            monsterX[i] = random.randint(30, 60)
            monsterY[i] = random.randint(0, 600)

        monster(monsterX[i], monsterY[i], i)

    # Movimiento de la bala
    if bulletX <= 0:
        bulletX = 600
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX -= bulletX_change

    soldier(soldierX, soldierY)
    show_score(textX, textY)

    pygame.display.update()


import sys
import random
import pygame

LARGURA = 800
ALTURA = 600
FPS = 60

FUNDO = (120, 120, 120)

QUIQUE = 1.0 

pygame.init() 

tela = pygame.display.set_mode((LARGURA, ALTURA)) 
pygame.display.set_caption("Pegue o Queijo") 
clock = pygame.time.Clock() 


rato = pygame.image.load("rato.png")
queijo = pygame.image.load("queijo.png")
inimigo = pygame.image.load("inimigo.png")

rato = pygame.transform.scale(rato, (80, 80))
queijo = pygame.transform.scale(queijo, (50, 50))
inimigo = pygame.transform.scale(inimigo, (70, 70))

rato_rect = rato.get_rect()
queijo_rect = queijo.get_rect()
inimigo_rect = inimigo.get_rect()

rato_rect.x = 100
rato_rect.y = 100

velocidade = 5

inimigo_rect.x = 600
inimigo_rect.y = 400
speed_inimigo = [2, 2]


pos = [float(random.randint(0, LARGURA - queijo_rect.width)), 0.0]
speed = [3.0, 0.0]
accel = [0.0, 0.5] 

som_queijo = pygame.mixer.Sound("queijo.wav") 
som_queijo.set_volume(10.0)
som_morte = pygame.mixer.Sound("morte.wav")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load("musica.wav")
pygame.mixer.music.play(-1, 0.0) 

pausado = False
queijos = 0 

TEMPO_RESPAWN = 2 * FPS
tempo_morte = 0

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                rato_rect.x = 100
                rato_rect.y = 100
                pos = [float(random.randint(0, LARGURA - queijo_rect.width)), 0.0]
                speed = [3.0, 0.0]
                inimigo_rect.x = 600
                inimigo_rect.y = 400
                tempo_morte = 0
                queijos = 0
            if evento.key == pygame.K_p:
                if pausado:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                pausado = not pausado
            if evento.key == pygame.K_s:
                pygame.mixer.music.stop()

    

    
    if tempo_morte == 0 and pygame.key.get_focused():
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            rato_rect.move_ip(-velocidade, 0)

        if teclas[pygame.K_RIGHT]:
            rato_rect.move_ip(velocidade, 0)

        if teclas[pygame.K_UP]:
            rato_rect.move_ip(0, -velocidade)

        if teclas[pygame.K_DOWN]:
            rato_rect.move_ip(0, velocidade)


    if rato_rect.left < 0:
        rato_rect.left = 0

    if rato_rect.right > LARGURA:
        rato_rect.right = LARGURA

    if rato_rect.top < 0:
        rato_rect.top = 0

    if rato_rect.bottom > ALTURA:
        rato_rect.bottom = ALTURA

 
    speed[0] = speed[0] + accel[0]
    speed[1] = speed[1] + accel[1]
  
    pos[0] = pos[0] + speed[0]
    pos[1] = pos[1] + speed[1]

    if pos[1] + queijo_rect.height > ALTURA:
        pos[1] = ALTURA - queijo_rect.height 
        speed[1] = -abs(speed[1]) * QUIQUE 

    if pos[0] < 0 or pos[0] + queijo_rect.width > LARGURA:
        pos[0] = max(0, min(pos[0], LARGURA - queijo_rect.width)) 
        speed[0] = -speed[0] 

    queijo_rect.topleft = (round(pos[0]), round(pos[1]))


    inimigo_rect.move_ip(speed_inimigo)

    if inimigo_rect.left < 0 or inimigo_rect.right > LARGURA:
        speed_inimigo[0] = -speed_inimigo[0]

    if inimigo_rect.top < 0 or inimigo_rect.bottom > ALTURA:
        speed_inimigo[1] = -speed_inimigo[1]


    if tempo_morte > 0:
        tempo_morte -= 1
        if tempo_morte == 0:
            rato_rect.x = 100
            rato_rect.y = 100
            inimigo_rect.x = 600
            inimigo_rect.y = 400

    if tempo_morte == 0 and rato_rect.colliderect(queijo_rect):
        som_queijo.play()
        queijos += 1
        pos = [float(random.randint(0, LARGURA - queijo_rect.width)), 0.0]
        speed = [3.0, 0.0]

    if tempo_morte == 0 and rato_rect.colliderect(inimigo_rect):
        print(f"Pego pelo inimigo! Voce tinha {queijos} queijos.")
        som_morte.play() # toca o som da morte
        queijos = 0
        tempo_morte = TEMPO_RESPAWN 

    pygame.display.set_caption("Pegue o Queijo | queijos = %d" % queijos)

    tela.fill(FUNDO) 
    if tempo_morte == 0:
        tela.blit(rato, rato_rect) 
    tela.blit(queijo, queijo_rect)
    tela.blit(inimigo, inimigo_rect)
    pygame.display.update() 
    clock.tick(FPS) 

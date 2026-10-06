import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pegue o Queijo")

rato = pygame.image.load("rato.png")
queijo = pygame.image.load("queijo.png")

rato = pygame.transform.scale(rato, (80, 80))
queijo = pygame.transform.scale(queijo, (50, 50))

rato_rect = rato.get_rect()
queijo_rect = queijo.get_rect()

rato_rect.x = 100
rato_rect.y = 100

queijo_rect.x = random.randint(0, LARGURA - queijo_rect.width)
queijo_rect.y = random.randint(0, ALTURA - queijo_rect.height)

velocidade = 5

som_queijo = pygame.mixer.Sound("queijo.wav")   
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load("musica.wav")           
pygame.mixer.music.play(-1, 0.0)                

rodando = True

clock = pygame.time.Clock()


while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        rato_rect.x -= velocidade

    if teclas[pygame.K_RIGHT]:
        rato_rect.x += velocidade

    if teclas[pygame.K_UP]:
        rato_rect.y -= velocidade

    if teclas[pygame.K_DOWN]:
        rato_rect.y += velocidade

    if rato_rect.left < 0:
        rato_rect.left = 0

    if rato_rect.right > LARGURA:
        rato_rect.right = LARGURA

    if rato_rect.top < 0:
        rato_rect.top = 0

    if rato_rect.bottom > ALTURA:
        rato_rect.bottom = ALTURA

    if rato_rect.colliderect(queijo_rect):

        queijo_rect.x = random.randint(0, LARGURA - queijo_rect.width)
        queijo_rect.y = random.randint(0, ALTURA - queijo_rect.height)

    tela.fill((230, 230, 230))

    tela.blit(rato, rato_rect)

    tela.blit(queijo, queijo_rect)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
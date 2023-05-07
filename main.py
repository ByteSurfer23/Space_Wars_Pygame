import pygame 
pygame.init()
screen = pygame.display.set_mode((800,800))
running = True 
pygame.display.set_caption("Castaway")
icon = pygame.image.load('totem.png')
pygame.display.set_icon(icon)
playerimg = pygame.image.load('traveller.png')
def player():
    playerX = 300
    playerY = 300
    screen.blit(playerimg,(playerX,playerY))
while running : 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    pygame.display.update()
    screen.fill((0,150,150))
    player()
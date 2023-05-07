import pygame 
import random
import math
from pygame import mixer 
pygame.init()
clock = pygame.time.Clock()

# bakcground music 
mixer.music.load('background.wav')
mixer.music.play(-1)

#creation of screen
screen = pygame.display.set_mode((800,600))
run = True

# game icon and title 
pygame.display.set_caption('Space Wars')
icon = pygame.image.load('spc.png')
pygame.display.set_icon(icon)

#player image 
player_img = pygame.image.load('plyr.png')
player_X=0
player_Y= 500
# player score 
player_score = 0
#player position 
def player_pos(x,y):
    screen.blit(player_img,(x,y))

villain_img = []
villain_X=[]
villain_Y=[]
vill_x_change=[]
vill_y_change=[]
num_of_vill = 5
"""here we create a loop for loading data about multiple enemies in a list and access it in the while loop to make 
multiple enemies appear in screen """
for i in range(num_of_vill):
    if i==2 or i==4:
        villain_img.append(pygame.image.load('villain_2.png'))# image of villain loading
        vill_x_change.append(3)# change in x value per frame 
        vill_y_change.append(50)# change in y value per frame 
    else:
        villain_img.append(pygame.image.load('villain.png'))# image of villain loading
        vill_x_change.append(1.5)# change in x value per frame 
        vill_y_change.append(50)# change in y value per frame 
    villain_X.append(random.randint(0,736))# random X value of villain so he respawns at a new place every time he dies
    villain_Y.append(random.randint(50,150))# random Y value of villain so he respawns at a new place every time he dies

"""initially we assign a value to vill_x_change , if u give it as 0 , on continuous iterations the value of villain_x
 does not change, on giving it a value villain_x undergoes additions repeatedly which may cause the villain to 
 move to the boundaries, on meeting bounds , vill_x_change takes a different value and hence changes direction
"""
# displaying the text in the screen, 
player_score=0
font = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y = 10

# putting text into screen
def show_score(x,y):
    score=font.render("Score: "+str(player_score),True,(255,255,255))
    screen.blit(score,(text_x,text_y))

#loading the background into the code 
bck_grnd = pygame.image.load('bg_3.png')

#displaying game over
over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

# villain position
def villain_pos(v_X,v_Y,n):
    screen.blit(villain_img[n],(v_X,v_Y))
x_change = 0

# bullet image load and initial position 
bullet_img = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

def bullet_pos(bullet_x,bullet_y):
    global bullet_state,bullet_img
    bullet_state="fire"
    screen.blit(bullet_img,(bullet_x,bullet_y))

"""for collision checking we use distance formula(root of x2-x1 whole sqr minus y2-y1 the whole sqr), 
if the bullet is present with in that radius with respect to the 
position of the villain then collision occurs"""
def has_it_collided(villain_X,villain_Y,bullet_X,bullet_Y):
    D = math.sqrt((villain_X - bullet_X)**2 + (villain_Y - bullet_Y)**2)
    if D<=20:
        return True
    else:
        return False
    
# actual working in the game screen in each frame 
while run:

    #setting screen colour and background 
    screen.fill((0,0,0))
    """bck_grnd is the image to be made as background and (0,0) refers the point from which the image is to filled 
    it will be filled till the end point(800,600)"""
    screen.blit(bck_grnd,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -4
            elif event.key == pygame.K_RIGHT:
                x_change = 4

        # bullet input through space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # for first frame it starts bullet x and bullet y from player x and player y
                # values at that instant of pressing space
                bullet_sound = mixer.Sound('gunshot.wav')#loads bullet sound into the pgm
                bullet_sound.play()#plays it when bullet is shot 
                bullet_X= player_X
                bullet_Y = player_Y 
                bullet_pos(bullet_X,bullet_Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

    # changing the value of x_change from + to - to prevent from leaving bounds 
    player_X += x_change
    if player_X <= 0:
        player_X = 0
    elif player_X>=736:
        player_X=736

    # changing the values of vill_x_change from + to - to prevent from leaving bounds
    # here villain_Y is also altered causing the alien to move by 50 pxs down on reaching bounds 
    for i in range(num_of_vill):
        if villain_Y[i]>=470:
            for j in range(num_of_vill):
                villain_Y[i] = 2000
            game_over_text()
            break
            
        villain_X[i] += vill_x_change[i]
        if villain_X[i] <= 0:
            if i ==2 or i==4:
                vill_x_change[i] = 4
            else:
                vill_x_change[i] = 1.5
            villain_Y[i]+=vill_y_change[i]
        elif villain_X[i]>=736:
            if i==2 or i==4:
                vill_x_change[i]=-4
            else:
                vill_x_change[i]=-1.5
            villain_Y[i]+=vill_y_change[i]

        collision = has_it_collided(villain_X[i],villain_Y[i],bullet_X,bullet_Y)# checking for collisions and alter villain at i
        if collision:
            vill_exp_sound = mixer.Sound('villain_expl.wav')# loads villain sound
            vill_exp_sound.play()# plays the sound 
            bullet_Y = 500
            bullet_state = "ready"
            villain_X[i] = random.randint(0,735)
            villain_Y[i] = random.randint(50,150)
            player_score += 1
        villain_pos(villain_X[i],villain_Y[i],i)

    if bullet_Y<=0:

        # if bullet_Y is goes to the top it comes back to the position of the spaceship and state becomes ready 
        bullet_Y=500
        bullet_state = "ready"

    # constant decrementing of y value of bullet position 
    if bullet_state == "fire":
        bullet_pos(bullet_X,bullet_Y)
        bullet_Y-=bullet_y_change
        if bullet_Y<=0:
            bullet_state="ready"
    
    #calling the postiton functions of ship and alien
    player_pos(player_X,player_Y)
    show_score(text_x,text_y)
    pygame.display.update()
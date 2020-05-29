# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:56:01 2020

@author: Yash
"""


import pygame
import random
import math
import os
pygame.init()

################## SCREEN AND DIMENSION####################
screen_width=800
screen_height=600
screen = pygame.display.set_mode((screen_width,screen_height))


################### Window bar info ##############
#------------Title-----------------------#
pygame.display.set_caption('Space Invader')
##################################################
#initalizes the clock
clock = pygame.time.Clock()

################### Loading in the assests #######
background = pygame.image.load(os.path.join('assets','background.png'))

player =  pygame.image.load(os.path.join('assets','spaceship.png'))

bullet =  pygame.image.load(os.path.join('assets','bullet.png'))
###################################################

# global declaration for the state of bullet
bullet_state = "ready"


########### Colors ###########
black=(0,0,0)
white = (255,255,255)
red = (200,0,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
##############################

######### Initializaion of Enemy##################
enemy=[]
no_of_enemies= 5
for ene in range (no_of_enemies):
    enemy.append( pygame.image.load(os.path.join('assets','alien.png')))
################################################## 

# global declaration of score
score_value =0

#################### FUCTIONS ####################


#Displays the start screen
def start_screen():
    
    intro =True
    
    while intro:
        screen.fill((12,12,12))
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
        largeText = pygame.font.SysFont('heartless',80)
        TextSurf, TextRect = text_objects("Space Invaders", largeText, (0,0,255))
        TextRect.center = ((screen_width/2),(screen_height/4))
        screen.blit(TextSurf, TextRect)
        
        Button("START",150,450,100,50,bright_green,green,black,play_game)  
        Button("QUIT",550,450,100,50,bright_red,red,black,pygame.quit)
           
        pygame.display.update()
        clock.tick(15)



# displays score
def show_score(x,y):
    font = pygame.font.SysFont('comicsansms',30)
    score = font.render('Score: '+ str(score_value),True,black)
    screen.blit(score,(x,y))
    

#creates player on screen
def show_player (x,y):
    screen.blit(player,(x,y))
    

#creates eneimies on the screen
def show_enemies(x,y,ene):
    screen.blit(enemy[ene],(x,y))

    
# Used to fire  the bullet and change its state
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'Fired'
    screen.blit(bullet,(x+16,y+10))


#checks for collison of bullet and enemy    
def check_collision(x,y,X,Y):
    distance = math.sqrt( (math.pow(x-X, 2)+math.pow(y-Y, 2)) )
    if distance <27:
        return True
    else:
        return False


# default text box and also getting its rectangle 
def text_objects(text , font, colour):
    textSurface = font.render(text, True , colour)
    return textSurface , textSurface.get_rect()


# Used to display the message
def message_display(text):

    largeText = pygame.font.SysFont('comicsansms',115)
    TextSurf, TextRect = text_objects(text, largeText , red)
    TextRect.center = ((screen_width/2),(screen_height/2))
    screen.blit(TextSurf, TextRect)
    
    Button("TRY AGAIN",150,450,150,50,bright_green,green,black,play_game)  
    Button("QUIT",550,450,100,50,bright_red,red,black,pygame.quit)
    pygame.display.update()
 
 
# runs after the game is over
def Game_over():
    
    outro = True
    
    while outro:
    
        screen.fill((0,128,255))
    
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                
        message_display('Game Over')
       
        pygame.display.update()
        
        
# Making a dynamic button
def Button(msg,x,y,w,h,ac,iac,mc,action=None):      
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #print(click)
        #print(mouse)

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
            if click[0]==1 and action!=None:
                action()
        else:
            pygame.draw.rect(screen, iac,(x,y,w,h))
                 
        smallText = pygame.font.SysFont("comicsansms",20,True)
        textSurf, textRect = text_objects(msg, smallText,mc)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)
        

# Pauses the game
def pause(state, player , no, x , y , cx):
    largeText = pygame.font.SysFont('comicsansms',115)
    TextSurf, TextRect = text_objects("Paused", largeText , red)
    TextRect.center = ((screen_width/2),(screen_height/2))
    screen.blit(TextSurf, TextRect)
    state = 'ready'
    player = 0
    
    for ene in range(no):
        if 0 < x[ene] < 736:
            x[ene]-=cx[ene]
            y[ene]=y[ene]
        

# Check if the game is to be paused
def check_pause():
    mouse = pygame.mouse.get_pos()
    #print (mouse)
  
    if  2 > mouse[0] or  mouse[0] > screen_width-2 or 2 > mouse[1] or  mouse[1] > screen_height-2 :
     return True
     

# The Main game group
def play_game():
    
    running =True
    ### all the game variable #####
    playerx =screen_width*0.45
    playery =screen_height*0.85
    change_player = 0
    
    enemyx=[]
    enemyy=[]
    change_enemy_X=[]
    change_enemy_Y=[]
    
    
    for ene in range(no_of_enemies):
        enemyx.append(random.randint(0, 736))
        enemyy.append( random.randint(0, 50))
        change_enemy_X.append(5)
        change_enemy_Y.append(32)
    
    bulletx =0
    bullety=480
    #change_bullet_X = 0
    change_bullet_Y = 7
    global bullet_state
    global score_value
    global clock
    
    
    textX=10
    textY=10
    #################################
    
    #the game loop
    while running:
       
           
        screen.fill((255,255,255,1))
        screen.blit(background,(0,0))
    
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_player=-6
                if event.key == pygame.K_RIGHT:
                    change_player=6
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletx=playerx
                        fire_bullet(bulletx, bullety)
               
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    change_player=0
                
                    
        playerx+=change_player
        
        if playerx<=0:
            playerx=0
       
        if playerx>=736:
            playerx=736
            
            
        for ene in range(no_of_enemies):
            
            if enemyy[ene] > 440:
                for j in range(no_of_enemies):
                    enemyy[j]=-2000
                    playery=-2000
                score_value=0
                bullet_state= 'ready'
                Game_over()
                break
            
            enemyx[ene]+=change_enemy_X[ene]
           
            if enemyx[ene]<0:
                change_enemy_X[ene]=5
                enemyy[ene]+=change_enemy_Y[ene]
            elif enemyx[ene]>736:
                change_enemy_X[ene]=-5
                enemyy[ene]+=change_enemy_Y[ene]
            
                
            collision = check_collision(enemyx[ene], enemyy[ene], bulletx, bullety)
            if collision:
                bullety = 480
                bullet_state="ready"
                score_value += 1
                
                enemyx[ene]=random.randint(0, 736)
                enemyy[ene] = random.randint(0, 50)
                
            show_enemies(enemyx[ene],enemyy[ene],ene)
            
            
        show_player(playerx,playery)
        
       
        if bullety<=0:
            bullety=480
            bullet_state="ready"
            
        if bullet_state == "Fired":
            fire_bullet(bulletx, bullety)
            bullety-=change_bullet_Y
    
    
    
        show_score(textX, textY)
        
        if check_pause():
            pause(bullet_state, change_player , no_of_enemies , enemyx , enemyy , change_enemy_X)
      
        pygame.display.update()
        clock.tick(60)
        
start_screen()    
pygame.quit()
quit()

import pygame
import time
import cargame
import snakegame
import Black_Jack_Game_Pack
import sys
black = (0,0,0)
white = (255,255,255)
grey = (50,50,50)
light_grey = (100,100,100)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
bright_yellow = (255,255,150)
light_yellow = (255,255, 230)
pygame.init()
display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Game Select")
gameIcon = pygame.image.load('gameSelectIcon.png')
clock = pygame.time.Clock()
logo = pygame.image.load('logo.png')
def button(msg, msg_color,x,y,w,h,ic,ac, size, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global chosing_game
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "dodging":
                cargame.game_start()
            if action == "snake":
                snakegame.game_start()
            if action == "blackjack":
                Black_Jack_Game_Pack.game_start()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    if size == "small":
        Text = pygame.font.Font("freesansbold.ttf",50)
    if size == "big":
        Text = pygame.font.Font("freesansbold.ttf",75)
        
    textSurf, textRect = text_objects(msg, Text, msg_color)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
chosing_game = True

def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
def start():
    pygame.display.set_caption("Game Select")
    pygame.display.set_icon(gameIcon)
    gameDisplay.fill((241, 188,8))
    pygame.display.update()
    time.sleep(.5)
    new_color = [0,0,0]
    x = [0,0,0]
    for i in range(100):
        if i < 50:
            new_color[0] += 1.9*2
            new_color[1] += 1.8*2
            new_color[2] += 1.4*2
            x[2] += 2.55*2
        else:
            new_color[0] -= 1.9*2
            new_color[1] -= 1.8*2
            new_color[2] -= 1.4*2
            x[2] -= 1*2
        gameDisplay.fill(new_color)
        gameDisplay.blit(logo, (0,0))
        pygame.display.set_icon(gameIcon.convert_alpha())
        gameDisplay.blit(gameIcon.convert_alpha(), (384,750))
        pygame.draw.rect(gameDisplay, new_color,(330,670,120,50))
        pygame.display.update()
        close()
        clock.tick(60)
    time.sleep(1)
    while chosing_game:
        pygame.display.set_caption("Game Select")
        pygame.display.set_icon(gameIcon)
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                pygame.quit()
                quit()
        gameDisplay.fill((190,179,140))
        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("GAME SELECT", largeText, (33,47,61))
        TextRect.center = ((display_width/2),(display_height/2)-300)
        gameDisplay.blit(TextSurf, TextRect)
        
        pygame.font.Font('freesansbold.ttf',100)
        
        mouse = pygame.mouse.get_pos()
        #small is for small text but big is for big text
        button("Dodger",black, 200, 175, 400, 150, (241, 188,8), yellow, "big", "dodging")
        button("Snake",black, 200, 350, 400, 150, (241, 188,8), yellow, "big", "snake")
        button("Black Jack",black,200, 525, 400, 150, (241, 188,8), yellow, "big", "blackjack")
        gameDisplay.blit(pygame.font.SysFont(None, 20).render("** Click escape to leave blackjack**", True, blue), (10,780))
        gameDisplay.blit(pygame.font.SysFont(None, 20).render("**X'ing out of window may result in return to this screen**", True, blue), (10,760))
        gameDisplay.blit(gameIcon, (384,750))
        pygame.display.update()
        clock.tick(15)
start()

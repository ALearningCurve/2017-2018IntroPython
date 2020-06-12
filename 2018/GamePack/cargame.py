"""
Esentially a dodge-the-obstacle game. This Code is very similiar to that of
the code at an educational video series under the name "aBitRacey" though there
are some differences such as an options menu, multiple cars, mouse controls and
multiple 'things' because of the 'thing' being a class. This code also will
save the highscore using a txt file so that the highscore will persist between
loads of the game.                   :^)
"""

import pygame
import time
import random

pygame.init()
display_width = 800
display_height = 800

#RGB ... You can have up to 255 for each color
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

colors = (white, red, bright_red, green, bright_red, blue, yellow, bright_yellow)
car_width = 65

gameDisplay = pygame.display.set_mode((display_width,display_height))
#pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()

thing_list = []
using_arrows = False


#TextTypes
largeText = pygame.font.Font('freesansbold.ttf',115)

#Load Cars and Set Default to Triangle Car
mariano = pygame.image.load('mariano.png')
atari = pygame.image.load('triangle.png')
racecar = pygame.image.load('car.png')
carImg = atari
gameIcon = pygame.image.load('carIcon.png')

def things_dodged(count):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Score: " + str(count), True, white)
    gameDisplay.blit(text, (0,0))

def close(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            import games
        
class high_score():
    #defualt font
    def __init__(self):
        self.best_score = 0
        t = open('carhighscore.txt','r+')
        for line in t:
            try:
                line = int(line.strip())
                if line > self.best_score:
                    self.best_score = line
            except:
                error = True
                
    def blit_high_score(self,count):
        font = pygame.font.SysFont(None, 50)
        if count > self.best_score:
            self.best_score = count
            with open('carhighscore.txt', 'r+') as file:
                file.write(str(self.best_score))
        text = font.render("Highscore: " + str(self.best_score), True, white)
        gameDisplay.blit(text, (0,50))

    def reset_score():
        with open('carhighscore.txt', 'r+') as file:
            file.write('0')
            
def button(msg, msg_color,x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global using_arrows
    global carImg
    
    global intro
    global pause
    global crash_loop
    global options
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "play":
                intro = False
                options = False
                game_loop()
            elif action == "quit":
                time.sleep(1)
                import games
                intro = False
                pause = False
                crash_loop = False
                options = False
                import games
                
            elif action == "unpause":
                pygame.mouse.set_visible(False)
                pygame.mixer.music.unpause()
                puase = False
                number = 3

                pygame.draw.rect(gameDisplay, grey,(100,400,250,100))
                pygame.draw.rect(gameDisplay, grey,(450, 400, 250, 100))
                for i in range(3):
                    
                    gameDisplay.fill(grey)
                    
                    largeText = pygame.font.SysFont("impact",300)
                    TextSurf, TextRect = text_objects(str(number), largeText, white)
                    TextRect.center = ((display_width/2),((display_height/2)))
                    gameDisplay.blit(TextSurf, TextRect)
                    pygame.display.update()
                    
                    time.sleep(1)

                    pygame.draw.rect(gameDisplay, grey,(display_width/2 - 125,display_height/2 - 125,250,250))
                    pygame.display.update()

                    number -= 1
                    gameDisplay.fill(grey)
                    
            elif action == "game_intro":
                options = False
                crash_loop = False
                time.sleep(.2)
                game_intro()
            elif action == "not using_arrows":
                using_arrows = False
            elif action == "is using_arrows":
                using_arrows = True
            #changes car's sprite
            elif action == "Atari":
                carImg = atari
            elif action == "RaceCar":
                carImg = racecar
            elif action == "Mariano":
                carImg = mariano
    #If the button has yet to be pressed....
    else:
        #Changes Color of the Button If Already Choosen
        if action == "not using_arrows":
            if using_arrows == False:
                ic = light_yellow
        elif action == "is using_arrows":
            if using_arrows == True:
                ic = light_yellow
        elif action == "Atari":
            if carImg == atari:
                ic = light_yellow
        elif action == "RaceCar":
            if carImg == racecar:
                ic = light_yellow
        elif action == "Mariano":
            if carImg == mariano:
                ic = light_yellow

        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",50)
    textSurf, textRect = text_objects(msg, smallText, msg_color)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

class things():
    def __init__(self):
        self.thing_height = 100
        self.thing_startx = random.randrange(-1 * self.thing_height, display_width)
        self.thing_starty = -600
        self.thing_speed = 8
        self.thing_width = 50
        self.color = random.randrange(100,255),random.randrange(100,255),random.randrange(100,255)
        self.thingx = self.thing_startx
        self.thingy = self.thing_starty

    #need x and y coordinates of the car
    def check(self, x,y, invulnerable):
        global dodged
        global car_width
        global car_speed
        global score


        #Check if off screen
        if self.thingy > display_height:
            self.thing_starty = 0 - self.thing_height
            self.thingy = self.thing_starty
            self.thing_startx = random.randrange(-1 * self.thing_height, display_width)
            self.thingx = self.thing_startx
            self.color = random.randrange(100,255),random.randrange(100,255),random.randrange(100,255)
            dodged += 1
            score += 1 * len(thing_list)

            if dodged == 2 and len(thing_list) < 2:
                thing_list.append(things())
            if dodged % 5 == 0 and len(thing_list) < 7:
                thing_list.append(things())
            if dodged %100 == 0:
                thing_list.append(things())

            #this is just to prevent the things from getting too fast/too wide
            if self.thing_speed < 21 and score < 2000:
                self.thing_speed += 1
                
            elif self.thing_speed < 24 and score >= 2000:
                self.thing_speed += 2
                
            if self.thing_width < 75 and score < 2000:
                self.thing_width += 5

            elif self.thing_width < 90 and score >= 2000:
                self.thing_width += 10
                
            if self.thing_speed == 20 and score < 2000:
                self.thing_speed = 10
                self.thing_width = 50

            if self.thing_speed ==  23 and score >= 2000:
                self.thing_speed = 15
                self.thing_width = 75
        #Check If Crashed into Car
        if y < self.thing_starty + self.thing_height -10 and y + 70 > self.thing_starty:

            if x+10 > self.thing_startx and x+10 < self.thing_startx + self.thing_width or x+car_width > self.thing_startx and x + car_width < self.thing_startx + self.thing_width:
                if not invulnerable:
                    global has_crashed
                    has_crashed = True
                    #return crash(score)

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.thingx, self.thingy, self.thing_width,self.thing_height])
        self.thing_starty += self.thing_speed
        self.thingy = self.thing_starty

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText, white)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def paused():
    pygame.mouse.set_visible(True)
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("impact",150)
    TextSurf, TextRect = text_objects("Paused", largeText,blue)
    TextRect.center = ((display_width/2),(display_height/2)-200)
    gameDisplay.blit(TextSurf, TextRect)
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause =  False
                    pygame.mouse.set_visible(False)
                if event.key == pygame.K_ESCAPE:
                    import games
            close(event)
        
        button("Continue", black, 275,400,250,100,green,bright_green,"unpause")
        #button("Back", black, 450,400,250,100,red,bright_red,"game_intro")

        pygame.display.update()
        clock.tick(15)

def options_menu():
    global options
    options = True
    pygame.mouse.set_visible(True)
    gameDisplay.fill(light_grey)

    largeText = pygame.font.SysFont("impact",155)
    TextSurf, TextRect = text_objects("OPTIONS", largeText, white)
    TextRect.center = ((display_width/2),((display_height/2)-325))
    gameDisplay.blit(TextSurf, TextRect)

    largeText = pygame.font.SysFont("impact",150)
    TextSurf, TextRect = text_objects("OPTIONS", largeText, black)
    TextRect.center = ((display_width/2),((display_height/2)-325))
    gameDisplay.blit(TextSurf, TextRect)
    
    while options:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    import games
            close(event)
        #Button to exit the options menu
        button("Start", black, 90,650,250,100,green,bright_green,"play")
        button("Back", black, 450,650,250,100,green,bright_green,"game_intro")

        #Control options
        button("Arrows", black, 400,200,250,50, yellow, bright_yellow, "is using_arrows")
        button("Mouse", black, 150,200,250, 50, yellow, bright_yellow, "not using_arrows")

        largeText = pygame.font.SysFont("impact",40)
        TextSurf, TextRect = text_objects("Controls", largeText, blue)
        TextRect.center = ((display_width/2), 175)
        gameDisplay.blit(TextSurf, TextRect)

        #Diferent Cars
        largeText = pygame.font.SysFont("impact",40)
        TextSurf, TextRect = text_objects("Cars", largeText, blue)
        TextRect.center = ((display_width/2), 350)
        gameDisplay.blit(TextSurf, TextRect)
        #Button to set Different Cars
        button("", black, 50,400, 200, 200, yellow, bright_yellow, "Atari")
        button("", black, 300,400, 200, 200, yellow, bright_yellow, "RaceCar")
        button("", black, 550,400, 200, 200, yellow, bright_yellow, "Mariano")

        gameDisplay.blit(atari, (113.5,460))
        gameDisplay.blit(racecar, (363.5,460))
        gameDisplay.blit(mariano, (613.5,460))

        pygame.display.update()
        clock.tick(15)

def crash(score):
    pygame.mouse.set_visible(True)
    button(" ", grey, 0,0,300,100,grey,grey)

    global thing_list
    thing_list = []

    #crash_sound = pygame.mixer.Sound("crash.wav")
    #pygame.mixer.music.stop()

    largeText = pygame.font.SysFont("impact",115)
    TextSurf, TextRect = text_objects("Game Over", largeText, yellow)
    TextRect.center = ((display_width/2),((display_height/2)-250))
    gameDisplay.blit(TextSurf, TextRect)

    largeText = pygame.font.SysFont("impact",60)
    TextSurf, TextRect = text_objects("Score: " +str(score), largeText, blue)
    TextRect.center = ((display_width/2),((display_height/2)-150))
    gameDisplay.blit(TextSurf, TextRect)

    largeText = pygame.font.SysFont("impact",60)
    TextSurf, TextRect = text_objects("Highscore: " + str(racey_highscore.best_score), largeText, blue)
    TextRect.center = ((display_width/2),((display_height/2)-50))
    gameDisplay.blit(TextSurf, TextRect)

    global crash_loop
    crash_loop = True
    while crash_loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    import games
            close(event)
        button("Again?", black, 150,400,200,100,green,bright_green,"play")
        button("Back", black, 450,400,200,100,red,bright_red,"game_intro")

        pygame.display.update()
        clock.tick(15)



def game_intro():
    
    pygame.mouse.set_visible(True)
    global intro
    intro = True
    
    global using_arrows

    gameDisplay.fill(grey)
    while intro:
        pygame.display.set_caption("Car Game")
        pygame.display.set_icon(gameIcon)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return options_menu()
                if event.key == pygame.K_ESCAPE:
                    import games
            close(event)


        background_carImg = pygame.image.load('background_carImg.png')
        gameDisplay.blit(background_carImg, (0,-100))

        largeText = pygame.font.Font('freesansbold.ttf',125)
        TextSurf, TextRect = text_objects("Car Game", largeText, yellow)
        TextRect.center = ((display_width/2),(display_height/2)-300)
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        button("GO!",black, 150, 650, 200, 100, green, bright_green, "play")
        button("Quit", black, 450, 650, 200, 100, red, bright_red, "quit")

        TextSurf, TextRect = text_objects("Space For Options", pygame.font.Font('freesansbold.ttf',25), (255,255,255))
        TextRect.center = (400,775)
        gameDisplay.blit(TextSurf, TextRect)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    pygame.mouse.set_visible(False)
    #pygame.mixer.music.load('jazz.wav')
    #pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    global score
    score = 0 
    global dodged
    dodged = 0
    global car_speed
    gameExit = False
    GodMode = False
    car_speed = 1
    thing_list.append(things())

    global has_crashed
    has_crashed = False
    while not gameExit:
        pygame.display.set_caption("Score: " + str(score) + "  |  " + "Highscore: " + str(racey_highscore.best_score))

        if has_crashed == True:
            return crash(score)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x > 0:
                    x_change = -10 - car_speed
                if event.key == pygame.K_RIGHT and x < display_width:
                    x_change = 10 + car_speed
                if event.key == pygame.K_u:
                    GodMode = False
                if event.key == pygame.K_i:
                    GodMode = False
                if event.key == pygame.K_p:
                    global pause
                    pause = True
                if event.key == pygame.K_ESCAPE:
                    import games

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            close(event)
        if using_arrows == True:
            x += x_change

        elif using_arrows == False:
            x = pygame.mouse.get_pos()[0] -35

        if score < 2000:
            gameDisplay.fill(grey)
        elif score > 2000:
            gameDisplay.fill(black)

        car(x,y)

        for thing in thing_list:
            thing.draw()

        for thing in thing_list:
            thing.check(x,y,GodMode)

        things_dodged(score)
        racey_highscore.blit_high_score(score)

        if x > display_width - car_width:
            x = display_width - car_width
        if x < 0:
            x = 0


        godMode = False
        pygame.display.update()
        clock.tick(60)

        
def game_start():
    time.sleep(.5)
    global racey_highscore
    racey_highscore = high_score()
    game_intro()



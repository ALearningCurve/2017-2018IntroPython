##Classic Snake game but with options for different skins, options, pause, a safe mode for preventing
##user error collsions [when they click two buttons too fast and turn snake into itself within one frame]

import random
import pygame
import time


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

snakeColor = green
pygame.init()
gameDisplay = pygame.display.set_mode((801,801))
fps = pygame.time.Clock()

gameIcon = pygame.image.load('snakeIcon.png')
optionsHelpMenu = pygame.image.load('Options Help -- Snake.jpg')
controlsHelpMenu = pygame.image.load('Controls Help -- Snake.jpg')
arrow = pygame.image.load('arrow.png')

randomAltImg = pygame.image.load('randomAlt.png')
rainbowAltImg = pygame.image.load('rainbowAlt.png')

bgAltImg = pygame.image.load('bgAlt.png')
rwbAltImg = pygame.image.load('rwbAlt.png')
ygbwAltImg = pygame.image.load('ygbwAlt.png')

need_to_strobe = False
need_to_alternate = False
altType = ""
safeMode = True

def draw_grid():
    for i in range(33):
        pygame.draw.rect(gameDisplay, black, ((0+25*i),0,3,800))
        pygame.draw.rect(gameDisplay, black, (0,(0+25*i),800,3))


def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def paused():
    pygame.mouse.set_visible(True)
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("impact",150)
    TextSurf, TextRect = text_objects("Paused", largeText,blue)
    TextRect.center = ((800/2),(800/2)-200)
    gameDisplay.blit(TextSurf, TextRect)
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause =  False
                    pygame.mouse.set_visible(False)
        button("Continue", black, 275,400,250,100,green,bright_green,"unpause")
        pygame.display.update()
        fps.tick(15)

def button(msg, msg_color,x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global snakeColor
    global pause
    global options
    global crash_loop
    global need_to_strobe
    global need_to_alternate
    global safeMode
    global altType
    global snake

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                time.sleep(1)
                global intro
                intro = False
                time.sleep(.2)
                import games
                

            elif action == "blue":
                snakeColor = blue
                need_to_strobe = False
                need_to_alternate = False

            elif action == "green":
                snakeColor = green
                need_to_strobe = False
                need_to_alternate = False

            elif action == "yellow":
                snakeColor = yellow
                need_to_strobe = False
                need_to_alternate = False

            elif action == "white":
                snakeColor = white
                need_to_strobe = False
                need_to_alternate = False


            elif action == "random":
                temp_list = []
                for i in range(3):
                    temp_list.append(random.randrange(1,255))
                snakeColor = temp_list
                need_to_strobe = False
                need_to_alternate = False

            elif action == "strobe":
                need_to_strobe = True
                need_to_alternate = False

            elif action == "randomAlt":
                altType = "randomAlt"
                need_to_alternate = True
                need_to_strobe = False

            elif action == "rainbowAlt":
                altType = "rainbowAlt"
                need_to_alternate = True
                need_to_strobe = False

            elif action == "bgAlt":
                altType = "bgAlt"
                need_to_alternate = True
                need_to_strobe = False

            elif action == "rwbAlt":
                altType = "rwbAlt"
                need_to_alternate = True
                need_to_strobe = False

            elif action == "ygbwAlt":
                altType = "ygbwAlt"
                need_to_alternate = True
                need_to_strobe = False

            elif action == "alternate":
                alt_menu()

            elif action == "unpause":
                pygame.mouse.set_visible(False)
                pygame.mixer.music.unpause()
                pause = False
                number = 3
                for i in range(4):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            time.sleep(.2)
                            import games
                            pygame.quit()
                            quit()
                            
                    gameDisplay.fill(black)
                    for pos in snake.getBody():
                        if pos == snake.position:
                            pygame.draw.rect(gameDisplay, grey, (pos[0],pos[1],25,25))
                        else:
                            if number-i == 3:
                                pygame.draw.rect(gameDisplay, red, (pos[0],pos[1],25,25))
                                color = red
                            elif number-i == 2:
                                pygame.draw.rect(gameDisplay, yellow, (pos[0], pos[1], 25,25))
                                color = yellow
                            elif number-i == 1:
                                pygame.draw.rect(gameDisplay, green, (pos[0], pos[1], 25,25))
                                color = green
                            else:
                                pygame.draw.rect(gameDisplay, blue, (pos[0], pos[1], 25,25))
                                color = blue
                                
                    pygame.draw.rect(gameDisplay, (250,0,0), (foodPos[0],foodPos[1],25,25))
                    draw_grid()

                    largeText = pygame.font.SysFont("impact",300)
                    TextSurf, TextRect = text_objects(str(number-i), largeText, color)
                    TextRect.center = ((800/2),((800/2)))
                    gameDisplay.blit(TextSurf, TextRect)
                    
                    pygame.display.update()
                    time.sleep(1)
                    pygame.display.update()
                    

            elif action == "game_intro":
                options = False
                pause = False
                crash_loop = False
                time.sleep(.2)
                game_intro()

            elif action == "safe":
                safeMode = True

            elif action == "risky":
                safeMode = False

    else:
        if action == "safe":
            if safeMode == True:
                ic = bright_yellow

        elif action == "risky":
            if safeMode == False:
                ic = bright_yellow

        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",50)
    textSurf, textRect = text_objects(msg, smallText, msg_color)
    textRect.center = ((x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    pygame.display.set_caption("Snake")
    pygame.mouse.set_visible(True)
    global intro
    intro = True

    gameDisplay.fill(black)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return options_menu()

                if event.key == pygame.K_c:
                    gameDisplay.fill(grey)
                    controlHelp = True
                    while controlHelp:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                time.sleep(.2)
                                import games
                                pygame.quit()
                                quit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_c:
                                    controlHelp = False
                                    continue

                        gameDisplay.blit(controlsHelpMenu, (0,0))
                        largeText = pygame.font.Font('freesansbold.ttf',30)
                        TextSurf, TextRect = text_objects("['C' To Go Back]", largeText, (255,255,255))
                        TextRect.center = (400,770)
                        gameDisplay.blit(TextSurf, TextRect)

                        fps.tick(15)
                        pygame.display.update()

        gameDisplay.fill(black)

        background_carImg = pygame.image.load('background_snakeImg.png')
        gameDisplay.blit(background_carImg, (150,225))
        #gameDisplay.fill(black)

        largeText = pygame.font.Font('freesansbold.ttf',125)
        TextSurf, TextRect = text_objects("Snake", largeText, (65,105,225))
        TextRect.center = ((800/2),(800/2)-300)
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = text_objects("Space For Options", largeText, (255,255,255))
        TextRect.center = (400,700)
        gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects("'C' For Controls", largeText, (255,255,255))
        TextRect.center = (400,750)
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()
        button("GO!",  black, 150, 550, 200, 100, green, bright_green, "play")
        button("Quit", black, 450, 550, 200, 100, red, bright_red, "quit")

        pygame.display.update()
        fps.tick(15)

def alt_menu():

    pygame.mouse.set_visible(True)
    global need_to_alternate
    global altType

    chosing = True

    while chosing:
        gameDisplay.fill(grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    chosing = False

        largeText = pygame.font.SysFont("impact",155)
        TextSurf, TextRect = text_objects("ALT. OPTIONS", largeText, red)
        TextRect.center = ((800/2),((800/2)-325))
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont("impact",50)
        TextSurf, TextRect = text_objects("Snake", largeText, white)
        TextRect.center = ((150),(185))
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont("impact",50)
        TextSurf, TextRect = text_objects("Appearance", largeText, white)
        TextRect.center = ((150),(235))
        gameDisplay.blit(TextSurf, TextRect)

        gameDisplay.blit(arrow, (300,170))

        if altType == "randomAlt":
            snakeAppearance = randomAltImg

        elif altType == "rainbowAlt":
            snakeAppearance = rainbowAltImg

        elif altType == "bgAlt":
            snakeAppearance = bgAltImg

        elif altType == "rwbAlt":
            snakeAppearance = rwbAltImg

        elif altType == "ygbwAlt":
            snakeAppearance = ygbwAltImg

        try:
            gameDisplay.blit(snakeAppearance, (450,200))
        except:
            largeText = pygame.font.SysFont("impact",25)
            TextSurf, TextRect = text_objects("(Select a Pattern)", largeText, yellow)
            TextRect.center = ((600),(215))
            gameDisplay.blit(TextSurf, TextRect)

        button("Random",    black, 50 ,300,325,75,(200,229,204),light_yellow,"randomAlt")
        button("Rainbow",   black, 430,300,325,75,(200,229,204),light_yellow,"rainbowAlt")


        button("Gold & Blue", black, 50 ,400,700,75,(200,229,204),light_yellow,"bgAlt")
        button("Red, White & Blue", black, 50,500,700,75,(200,229,204),light_yellow,"rwbAlt")
        button("Yellow/Green/Blue/White"  , black, 50,600,700,75,(200,229,204),light_yellow,"ygbwAlt")

        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = text_objects("['B' To Go Back]", largeText, (255,255,255))
        TextRect.center = (400,770)
        gameDisplay.blit(TextSurf, TextRect)

        fps.tick(15)
        pygame.display.update()

def options_menu():
    pygame.mouse.set_visible(True)
    global options
    options = True

    global need_to_alternate
    global need_to_strobe
    while options:
        gameDisplay.fill(grey)

        if need_to_alternate == False and need_to_strobe == False:
            largeText = pygame.font.SysFont("impact",155)
            TextSurf, TextRect = text_objects("OPTIONS", largeText, snakeColor)
            TextRect.center = ((800/2),((800/2)-325))
            gameDisplay.blit(TextSurf, TextRect)

            largeText = pygame.font.SysFont("impact",40)
            TextSurf, TextRect = text_objects("- This is the Current Color -", largeText, snakeColor)
            TextRect.center = ((800/2), 170)
            gameDisplay.blit(TextSurf, TextRect)

        elif need_to_alternate == True or need_to_strobe == True:
            largeText = pygame.font.SysFont("impact",155)
            TextSurf, TextRect = text_objects("OPTIONS", largeText, (0,0,0))
            TextRect.center = ((800/2),((800/2)-325))
            gameDisplay.blit(TextSurf, TextRect)

            if need_to_strobe == True:
                largeText = pygame.font.SysFont("impact",40)
                TextSurf, TextRect = text_objects("- Color Will Strobe -", largeText, (255,0,0))
                TextRect.center = ((800/2), 170)
                gameDisplay.blit(TextSurf, TextRect)

            elif need_to_alternate == True:
                largeText = pygame.font.SysFont("impact",40)
                TextSurf, TextRect = text_objects("- Color Will Alternate -", largeText, (255,0,0))
                TextRect.center = ((800/2), 170)
                gameDisplay.blit(TextSurf, TextRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    help = True
                    gameDisplay.fill(grey)
                    while help:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                time.sleep(.2)
                                import games
                                pygame.quit()
                                quit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_h:
                                    gameDisplay.fill(grey)
                                    help = False
                                    continue
                        gameDisplay.blit(optionsHelpMenu, (0,0))
                        largeText = pygame.font.Font('freesansbold.ttf',30)
                        TextSurf, TextRect = text_objects("['H' To Go Back]", largeText, (255,255,255))
                        TextRect.center = (400,770)
                        gameDisplay.blit(TextSurf, TextRect)

                        fps.tick(15)
                        pygame.display.update()

        button("Random", black, 25 ,200,230,75,(200,229,204),light_yellow,"random")
        button("Strobe", black, 280,200,230,75,(200,229,204),light_yellow,"strobe")
        button("Alt."  , black, 530,200,230,75,(200,229,204),light_yellow,"alternate")

        #Button to set Different Color Snake
        button("", black, 25 ,340, 150, 150, blue, blue, "blue")
        button("", black, 225,340, 150, 150, bright_green, bright_green, "green")
        button("", black, 425,340, 150, 150, yellow, yellow, "yellow")
        button("", black, 625,340, 150, 150, white, white, "white")

        button("Risky", black, 400,550,250,75, yellow, light_yellow, "risky")
        button("Safe", black, 150,550,250, 75, yellow, light_yellow, "safe")

        button("Start", black, 90,650,250,100,green,bright_green,"play")
        button("Back", black, 450,650,250,100,green,bright_green,"game_intro")

        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = text_objects("['H' For Options Help]", largeText, (255,255,255))
        TextRect.center = (400,770)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        fps.tick(15)

def crash(score):
    pygame.mouse.set_visible(True)

    #crash_sound = pygame.mixer.Sound("crash.wav")
    #pygame.mixer.music.stop()

    largeText = pygame.font.SysFont("impact",115)
    TextSurf, TextRect = text_objects("Game Over", largeText, (245,222,179))
    TextRect.center = ((800/2),((800/2)-250))
    gameDisplay.blit(TextSurf, TextRect)

    largeText = pygame.font.SysFont("impact",60)
    TextSurf, TextRect = text_objects("Score: " +str(score), largeText, (173,216,230))
    TextRect.center = ((800/2),((800/2)-150))
    gameDisplay.blit(TextSurf, TextRect)

    largeText = pygame.font.SysFont("impact",60)
    TextSurf, TextRect = text_objects("Highscore: " + str(highScore.best_score), largeText, (173,216,230))
    TextRect.center = ((800/2),((800/2)-50))
    gameDisplay.blit(TextSurf, TextRect)

    global crash_loop
    crash_loop = True
    while crash_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        button("Again?", black, 150,400,200,100,green,bright_green,"play")
        button("Back", black, 450,400,200,100,red,bright_red,"game_intro")

        pygame.display.update()
        fps.tick(15)

class Snake():
    def __init__(self):
        self.add8 = 8
        self.position = [100,50]
        self.body = []
        self.direction = "RIGHT"

    def changeDirectionTo (self, direction):
        if direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 25
        if self.direction == "LEFT":
            self.position[0] -= 25
        if self.direction == "UP":
            self.position[1] -= 25
        if self.direction == "DOWN":
            self.position[1] += 25
        self.body.insert(0,self.position[:])
        if self.position == foodPos:
            self.add8 = 0
            return 1
        elif self.add8 > 8:
            self.body.pop()
            return 0
        self.add8 += 1

    def checkCollision(self):
        if self.position[0] > 775:
            self.position[0] = 0
        elif self. position[0] < 0:
            self.position[0] = 775
        elif self.position[1] > 775:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = 775
        for bodyPart in self.body[1:]:
            if self.body[0] == bodyPart:
                return 1
        return 0
    def checkTeleport(self):
        for body in self.body[1:]:
            if body[0] > 775:
                body[0] = 0
            elif body[0] < 0:
                body[0] = 775
            elif body[1] > 775:
                body[1] = 0
            elif body[1] < 0:
                body[1] = 775
    def getHeadPos(self):
        return self.position
    def getBody(self):
        return self.body

class FoodSpawner():
    def __init__(self):
        self.position = [200,50]#[random.randrange(1,32)*25, random.randrange(1,32)*25]
        self.isFoodOnScreen = True
    def spawnFood(self):
        global snake
        while self.isFoodOnScreen == False:
            self.position = [random.randrange(1,32)*25, random.randrange(1,32)*25]
            self.isFoodOnScreen = True
        overlapping = True
        snakeBody = snake.getBody()
        bodyCount = 1
        while overlapping:
            for body in snakeBody[1:]:
                if [body[0],body[1]] == self.position:
                    self.position = [random.randrange(1,32)*25, random.randrange(1,32)*25]
                else:
                    bodyCount += 1

            if bodyCount >= len(snakeBody):
                overlapping = False
                self.isFoodOnScreen = True
                return self.position
            else:
                bodyCount = 1
            

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b

class HighScore():
    def __init__(self):
        self.best_score = 0
        t = open('snakehighscore.txt', 'r+')
        for line in t:
            if int(line) > self.best_score:
                self.best_score = int(line)
    def update_high_score(self,count):
        if count > self.best_score:
            self.best_score = count
            with open('snakehighscore.txt', 'r+') as file:
                file.write(str(self.best_score))
    def reset_score(self):
        with open('snakehighscore.txt','r+') as file:
            file.write('0')


def game_loop():
    global snakeColor
    score = 0
    pygame.mouse.set_visible(False)
    global foodSpawner
    global foodPos
    foodSpawner = FoodSpawner()
    global snake
    snake = Snake()
    global need_to_strobe
    global need_to_alternate
    a_key_is_down = False
    global altType
    colorListPos = 0
    alternateList = []
    while True:
        if need_to_strobe == True:
            temp_list = []
            for i in range(3):
                temp_list.append(random.randrange(1,255))
            snakeColor = temp_list
        if need_to_alternate == True:
            #snakeLength = snake.getBody()
            #if altType == "randomAlt":
            if len(snake.getBody()) >= len(alternateList):
                if altType == "randomAlt":
                    temp_list = []
                    for i in range(3):
                        temp_list.append(random.randrange(1,255))
                    alternateList.append(temp_list)
                if altType == "rainbowAlt":
                    rainbowList = [(255,0,0),    #red
                                   (255,128,0),  #orange
                                   (255,255,0),  #yellow
                                   (128,255,0),  #green
                                   (0,128,225),  #blue
                                   (0,0,255),    #indigo
                                   (127,0,255)   #violet
                                   ]
                    alternateList.append(rainbowList[colorListPos])
                    colorListPos += 1
                    if colorListPos >= 7:
                        colorListPos = 0
                if altType == "bgAlt":
                    blueGoldList = [(0,0,204),
                                    (204,204,0)
                                    ]
                    alternateList.append(blueGoldList[colorListPos])
                    colorListPos += 1
                    if colorListPos >= 2:
                        colorListPos = 0
                if altType == "rwbAlt":
                    redWhiteBlueList = [(255,0,0),
                                        (255,255,255),
                                        (0,0,255)
                                        ]
                    alternateList.append(redWhiteBlueList[colorListPos])
                    colorListPos += 1
                    if colorListPos >= 3:
                        colorListPos = 0
                if altType == "ygbwAlt":
                    yellowGreenBlueWhite = [(255,255,0),
                                            (128,255,0),
                                            (0,128,255),
                                            (255,255,255)
                                            ]
                    alternateList.append(yellowGreenBlueWhite[colorListPos])
                    colorListPos += 1
                    if colorListPos >= 4:
                        colorListPos = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(.2)
                import games
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and not a_key_is_down:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.changeDirectionTo("RIGHT")
                    if safeMode == True:
                        a_key_is_down = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.changeDirectionTo("LEFT")
                    if safeMode == True:
                        a_key_is_down = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.changeDirectionTo("UP")
                    if safeMode == True:
                        a_key_is_down = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.changeDirectionTo("DOWN")
                    if safeMode == True:
                        a_key_is_down = True
                if event.key == pygame.K_p:
                    global pause
                    pause = True
                    paused()
        #for foodSpawner in foodList:
        foodPos = foodSpawner.spawnFood()
        if snake.move(foodPos) == 1:
            score += 1
            foodSpawner.setFoodOnScreen(False)
        if snake.checkCollision() == 1:
            return crash(score)
        snake.checkTeleport()
        gameDisplay.fill(black)
        indexPos = 0
        for pos in snake.getBody():
            if pos == snake.position:
                pygame.draw.rect(gameDisplay, white, (pos[0],pos[1],25,25))
            else:
                if need_to_alternate != True:
                    pygame.draw.rect(gameDisplay, snakeColor, (pos[0],pos[1],25,25))
                elif need_to_alternate == True:
                    pygame.draw.rect(gameDisplay, alternateList[indexPos], (pos[0],pos[1],25,25))
            indexPos += 1
        pygame.draw.rect(gameDisplay, (250,0,0), (foodPos[0],foodPos[1],25,25))
        pygame.draw.rect(gameDisplay, (120,120,120), (snake.position[0], snake.position[1], 25,25))
        draw_grid()
        highScore.update_high_score(score)
        pygame.display.set_caption("Score: " + str(score) + "   |   " + "Highscore: " + str(highScore.best_score))
        pygame.display.update()
        a_key_is_down = False
        fps.tick(10)

def game_start():
    time.sleep(.5)
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(gameIcon)
    global highScore
    highScore = HighScore()
    game_intro()



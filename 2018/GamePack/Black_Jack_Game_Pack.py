'''
Blackjack: William Walling-Sotolongo 5/3/2018  C-Block Mr.Lavigne
This game works with pygame, still has print statements and not kivy.
'''

import random
import pygame
import time
import sys
import os
sys.path.insert(0, 'C:/Users/21wwalling-sotolongo/Desktop/Python Projects/Black Jack/Images')


pygame.init()
stop_loop = False

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

playerStand = False
dealerStand = False

class HighScore():
    def __init__(self):
        t = open('bjhighscore.txt')#, 'w+')
        self.best_score = -1
        self.best_name = ""
        for line in open('bjhighscore.txt', 'r+'):
            if int(line[:line.find("+~#~+")]) > self.best_score:
                self.best_score = int(line[:line.find("+~#~+")])
                self.best_name = line[line.find("+~#~+")+5:]
    def update_high_score(self,count):
        if count > self.best_score:
            self.reset_score()
            self.best_score = player.bankroll
            with open('bjhighscore.txt', 'r+') as file:
                file.write(str(self.best_score) + "+~#~+" + player.name)
            self.best_name = player.name
        pygame.display.set_caption("Blackjack   |   Best Score: $" + str(self.best_score) + " by " + self.best_name)
    def reset_score(self):
        os.remove('bjhighscore.txt')
        open('bjhighscore.txt', 'w+')
        with open('bjhighscore.txt','r+') as file:
            file.write('0+~#~+N')
        pygame.display.set_caption("Blackjack   |   Best Score: $" + str(self.best_score) + " by " + self.best_name)

highScore = HighScore()
class Card:
    def __init__(self, suit, value, hidden, location):
        self.suit = suit
        self.value = value
        self.name = str(value)
        self.hidden = hidden
        self.location = location
        self.img = None
        self.hiddenImg = pygame.image.load('blue_back.png')
        if self.name == "11":
            self.name = "Jack"
            self.value = 10

        elif self.name == "12":
            self.name = "Queen"
            self.value = 10

        elif self.name == "13":
            self.name = "King"
            self.value = 10

        elif self.name == "14":
            self.value = 11
            self.name = "Ace"

    def __repr__(self):
        info  = str(self.name) + " of " + str(self.suit)
        info =  (str(self.name) + " of " + str(self.suit))
        if self.hidden == True:
            info = "-----"
        return info

    def image(self):
        image = self.img
        if self.hidden == True:
            image = self.hiddenImg
        return image
    def info(self):
        info = str(self.name) + " of " + str(self.suit)
        if self.hidden == True:
            info = "-----"
        return info


class Deck:
    def __init__(self):
        self.cardSuits = ["Hearts", "Diamond", "Spades", "Clubs"]
        self.cardList = []
        self.generate_deck()
        self.shuffle()

    def generate_deck(self):
        self.cardList = []
        for i in range(4):
            for number in range(2,15):
                self.cardList.append(Card(self.cardSuits[i],number,False, len(self.cardList )))
        cardImages = []
        for card in self.cardList:
            try:
                imgName = card.name[0]+card.suit[0] +".png"
                cardImages.append(pygame.image.load(imgName))
            except:
                imgName = card.name[:2]+card.suit[0] +".png"
                cardImages.append(pygame.image.load(imgName))
        for i in range(52):
            self.cardList[i].img = cardImages[i]

    def shuffle(self):
        self.generate_deck()
        temp = []
        while len(self.cardList) > 0:
            x = random.choice(self.cardList)
            temp.append(x)
            self.cardList.remove(x)
        self.cardList = temp

    def return_card (self, hand):
        for card in hand:
            self.cardList.append(card)
        hand = []
        return hand

    def draw_top(self, hidden):
        topCard = self.cardList[0]
        topCard.hidden = hidden
        self.cardList.pop(0)
        return topCard

    def deal(self, hand):
        hand.append(self.draw_top(False))
        hand.append(self.draw_top(True))
        return hand

    def check_deck(self):
        if len(self.cardList) == 52:
            return True
        else:
            return False

    def __repr__(self):
        return str(len(self.cardList)) + " cards remain in the deck"

class Hand():
    def __init__(self, usr):
        self.usr = usr
        self.cards = []
        self.cards2 = []
        self.handWorth = 0
        self.splitted = False

    def get_hand_worth(self, cards = ""):
        if cards == "":
            cards = self.cards
        self.handWorth = 0
        for card in cards:
            self.handWorth = card.value + self.handWorth
        return self.handWorth

    def hit(self,hidden):
        self.get_hand_worth()
        if self.get_hand_worth()< 21:
            card = deck.draw_top(hidden)
            if card.name == "Ace" and self.get_hand_worth() > 10:
                card.value = 1
            self.cards.append(card)

        if self.splitted == True and self.get_hand_worth(self.cards2)<21:
            card = deck.draw_top(hidden)
            if card.name == "Ace" and self.get_hand_worth(self.cards2) > 10:
                card.value = 1
            self.cards2.append(card)

    def restart(self):
        temp = []
        temp = deck.return_card(self.cards)
        self.cards = temp

        temp = []
        temp = deck.return_card(self.cards2)
        self.cards2 = temp
        self.splitted = False


    def hand_info(self,end = ""):
        if self.usr == "player" or end == True:
            for card in self.cards:
                card.hidden = False
            for card in self.cards2:
                card.hidden = False
        temp = ""
        for card in self.cards[:-1]:
            temp = temp + card.info() + ", "
        temp = temp + self.cards[-1].info()

        if self.splitted:
            temp = temp + "     Second Hand: "
            for card in self.cards2[:-1]:
                temp = temp + card.info() + ", "
            temp = temp + self.cards2[-1].info()
        self.get_hand_worth()
        return temp


    def __repr__(self):
        return self.hand_info()

class Player():
    def __init__(self):
        self.hand = Hand("player")
        self.name = name
        self.bankroll = 2000
        self.bet = 0
        global playerStand
        playerStand = False
        hm = 20
        self.buttons = [Button("Hit", white,        500, 10 , 250, 60, grey , white, self.hand.hit, False),
                        Button("Stand", white,      500, 85 , 250, 60, grey , white, self.stand),
                        Button("Double Down", white,500, 160, 250, 60, grey , white, self.double_down),
                        Button("Split", white,      500, 235, 250, 60, grey , white, self.split),

                        Button("$1", white,      500, 500+hm, 125, 60, grey , white, 'x',1),
                        Button("$10", white,     650, 500+hm, 125, 60, grey , white, 'x',10),
                        Button("$100", white,    500, 575+hm, 125, 60, grey , white, 'x',100),
                        Button("$1000", white,   650, 575+hm, 125, 60, grey , white, 'x',1000),
                        Button("Deal", white,    500, 650+hm, 275, 60, grey , white, 'x','break' )
        ]


    def restart(self):
        self.hand.restart()
        global playerStand
        playerStand = False
        global dealerStand
        dealerStand = False

    def stand(self):
        self.hand.get_hand_worth()
        global playerStand
        playerStand = True
        return self.hand.handWorth

    def show(self, word):
        if word == "bankroll":
            return (self.name + " has a bankroll of $" + str(self.bankroll) + ".")

        elif word == "bet":
            return (self.name + " is betting $" + str(self.bet))

        elif word == "loss":
            return random.choice([(self.name + " just got wrecked"),(self.name + " just got beaned"), (self.name + " belongs in the trash"),(player.name + " isn't very goodaru")])

        elif word == "win":
            return random.choice([(self.name + " is victorous!"),("EZ dub for " + self.name), (self.name + " is just too good")])

    def update_bankroll(self, result):
        if result == "player":
            self.bankroll = self.bankroll + self.bet

        elif result == "dealer":
            self.bankroll = self.bankroll - self.bet

        elif result == "tie":
            pass
        else:
            return "Other Result [Error]: " + result

    def wager(self):
        self.bet = 0
        while True:
            pygame.display.update()
            for button in self.buttons[4:8]:
                x = False
                if not button.parameter + self.bet > self.bankroll:
                    x = button.check()
                else:
                    button.hide()
                if x:
                    self.bet += button.parameter
            if self.bet > 0 and self.buttons[8].check() == 'break':
                self.buttons[8].hide()
                break

            clock.tick(10)

            pygame.draw.rect(gameDisplay, green,(0,750,800,50))
            font = pygame.font.SysFont(None, 40)
            gameDisplay.blit(font.render(player.name + ",", True, white,green), (500,450))
            gameDisplay.blit(font.render("Enter your bet! ", True, white,green), (500,482.5))
            font = pygame.font.SysFont(None, 25)
            gameDisplay.blit(font.render(player.show('bankroll'), True, white,green), (10,750))
            gameDisplay.blit(font.render(player.show('bet'), True, white,green), (450,750))
            pygame.display.update()
            close()
        time.sleep(.2)

    def split(self, check = False):
        if not player.hand.splitted:
            if self.hand.cards[0].name == self.hand.cards[1].name:
                if check:
                    return True
                self.hand.cards2.append(self.hand.cards[1])
                self.hand.cards.pop(1)
                self.hand.splitted = True


    def double_down(self, check = False):
        doubledMoney = self.bet * 2
        if check and doubledMoney <= self.bankroll:
            return True
        doubledMoney = self.bet * 2
        if not doubledMoney > self.bankroll:
            self.bet = doubledMoney
            self.hand.hit(False)
            self.stand()
            return True
        else:
            return False

    def take_turn(self):
        while True:
            for button in self.buttons[:2]:
                if button.check():
                    return
            if self.split(True):
                if self.buttons[3].check():
                    return
            if self.double_down(True):
                if self.buttons[2].check():
                    return

class Dealer(Player):
    def __init__(self):
        self.hand = Hand("dealer")
        self.name = "Dealer"
        self.bankroll = None
        self.bet = None
        global dealerStand
        dealerStand = False

    def stand(self):
        self.hand.get_hand_worth()
        global dealerStand
        dealerStand = True
        for card in self.hand.cards[:]:
            card.hidden = False
        for i in range(len(self.hand.cards)):
            gameDisplay.blit(self.hand.cards[i].image(), (50+i*50,100))
            pygame.display.update()
            close()

        pygame.draw.rect(gameDisplay, green, [0,50, 800,40])

        font = pygame.font.SysFont(None, 50)
        gameDisplay.blit(font.render("Hand Value: " + str(dealer.hand.get_hand_worth()), True, white), (10,50))
        pygame.display.update()
        close()
        return self.hand.handWorth

    def turn_last_card(self):
        for card in self.hand.cards[:-1]:
                card.hidden = False

    def take_turn(self):
        self.hand.get_hand_worth()
        if self.hand.handWorth <= 16:
            self.hand.hit(False)
            self.turn_last_card()
            return(True)

        elif self.hand.handWorth >= 17:
            self.stand()
            return(False)

    def show(self,word):
        if word == "bankroll":
            return (self.name + " has no bankroll")

        elif word == "bet":
            return (self.name + " cannot bet")

        elif word == "loss":
            return random.choice([("The " + self.name + " just got wrecked"),("The " + self.name + " just got beaned"), ("The " + self.name + " belongs in the trash"),("The " + self.name + " isn't very goodaru")])

        elif word == "win":
            return random.choice([("The " + self.name + " is victorous!"),("EZ dub for the " + self.name), ("The " + self.name + " is just too good")])


    def wager(self):
        pass
    def update_bankroll(self, win, amount = None):
        pass
    def split(self):
        pass
    def double_down(self):
        pass

class Game():
    def __init__(self):
        gameDisplay.fill(green)
        self.turnList = []
        self.create()
        self.winner = ""
        self.cardCount = 0
        self.game()

    def create(self):
        global player
        global dealer
        global deck
        deck = Deck()
        player = Player()
        dealer = Dealer()

    def new_deck(self):
        deck.shuffle()

    def check(self):
        Worth1 = player.hand.get_hand_worth()
        Worth2 = player.hand.get_hand_worth(player.hand.cards2)
        pWorth = [Worth1, Worth2]
        dWorth = dealer.hand.get_hand_worth()

        for i in range(1):
            if dWorth > 21:
                if pWorth[0]>21 and pWorth[1]>21 and player.hand.splitted == True:
                    self.winner = "tie"
                elif pWorth[0]>21:
                    self.winner = "tie"
                else:
                    self.winner = "player"
                    break

            elif pWorth[0] > dWorth and pWorth[0] <= 21:
                self.winner = "player"
                break
            elif pWorth[1] > dWorth and pWorth[1] <= 21:
                self.winner = "player"
                break
            elif pWorth[0]> 21 and not player.hand.splitted:
                self.winner = "dealer"
            elif pWorth[0]>21 and pWorth[1]>21:
                self.winner = "dealer"
            elif pWorth[0] < dWorth and pWorth[1] < dWorth:
                self.winner = "dealer"
            elif pWorth[0] == dWorth:
                if player.hand.splitted and pWorth[1] == dWorth:
                    self.winner = "tie"
                elif not player.hand.splitted:
                    self.winner = "tie"
            elif pWorth[0] > 21 and pWorth[1] < dWorth:
                self.winner = "dealer"
            elif pWorth[1] > 21 and pWorth[0] < dWorth:
                self.winner = "dealer"
            else:
                self.winner = "error"

        if self.winner == "tie":
            self.winner = "dealer"
            text = "Tie!"
            color = red
        elif self.winner == "player":
            text = random.choice([player.show("win"), dealer.show("loss")])
            color = blue
        elif self.winner == "dealer":
            color = red
            text = random.choice([player.show("loss"), dealer.show("win")])
        else:
            text = self.winner
            color = yellow
        font = pygame.font.SysFont(None, 50)
        gameDisplay.blit(font.render(text, True, color, None), (10,350))
        player.update_bankroll(self.winner)
        font = pygame.font.SysFont(None, 25)
        gameDisplay.blit(font.render(player.show('bankroll'), True, white, green), (10,750))
        gameDisplay.blit(font.render(player.show('bet'), True, white, green), (450,750))
        highScore.update_high_score(player.bankroll)
        pygame.display.update()
        close()


    def game_message(self):
        gameDisplay.fill(green)
        font = pygame.font.SysFont(None, 50)
        pygame.draw.rect(gameDisplay, green,(0,750,800,75))

        for i in range(len(dealer.hand.cards)):
            gameDisplay.blit(dealer.hand.cards[i].image(), (50+i*50,100))
            text = font.render("Hand Value: ????", True, white)
            gameDisplay.blit(text, (10,50))
            text = font.render(dealer.name+"\'s hand", True, white)
            gameDisplay.blit(text, (10,10))
            pygame.display.update()
            close()

        for i in range(len(player.hand.cards)):
            if not player.hand.splitted:
                text = font.render("Hand Value: " + str(player.hand.get_hand_worth()), True, white)
                gameDisplay.blit(player.hand.cards[i].image(), (50+i*50,550))
            else:
                text = font.render("Hand Value: " + str(player.hand.get_hand_worth()) + " and " + str(player.hand.get_hand_worth(player.hand.cards2)), True, white)
                gameDisplay.blit(player.hand.cards[i].image(), (50+i*25,550))
                gameDisplay.blit(player.hand.cards2[i].image(),((150+i*25)+25*len(player.hand.cards2),550))
            gameDisplay.blit(text, (10,500))
            text = font.render(player.name+"\'s hand", True, white)
            gameDisplay.blit(text, (10,460))
            pygame.display.update()
            close()
        font = pygame.font.SysFont(None, 25)
        gameDisplay.blit(font.render(player.show('bankroll'), True, white), (10,750))
        gameDisplay.blit(font.render(player.show('bet'), True, white), (450,750))
        pygame.display.update()
        close()

    def take_turns(self):
        global playerStand
        global dealerStand
        self.game_message()
        while playerStand == False:
            if player.hand.get_hand_worth() == 21 or player.hand.get_hand_worth(player.hand.cards2) == 21:
                playerStand = True
                break
            if not playerStand:
                player.take_turn()
            self.game_message()

            if player.hand.get_hand_worth() > 21:
                if not player.hand.splitted:
                    break
            if player.hand.get_hand_worth(player.hand.cards2) > 21 and player.hand.get_hand_worth() > 21:
                break
        dealer.hand.hand_info(True)
        while not dealerStand:
            dealer.take_turn()

    def text_objects(self, text, font,color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def game(self):
        button = Button("Restart???", white, 275, 600, 250, 60, grey , white, self.__init__)
        while True:
            deck.deal(player.hand.cards)
            player.hand.cards[1].hidden = False
            deck.deal(dealer.hand.cards)
            player.wager()
            self.take_turns()
            self.check()
            if player.bankroll == 0:

                time.sleep(1.5)
                gameDisplay.fill(green)
                smallText = pygame.font.SysFont(None, 50)
                msgList = ["RIP, there was never a story of more woe",
                "than that of Juliet and her Gnomeo",
                "Except for that of " + player.name,
                "[Cuz you ran out of Doge Coins]",
                "*You Have Been Kicked Out Of The Casino*",
                "You should have just spent that money on ",
                "Fortnite..."
                ]
                for i in range(len(msgList)):
                    textSurf, textRect = self.text_objects(msgList[i], smallText, white)
                    textRect.center = (400, 300 + 40 * i)
                    gameDisplay.blit(textSurf, textRect)

                while True:
                    if button.check():
                       break
                    pygame.display.update()
                    close()
            self.restart()

    def restart(self):
        turns.update(len(self.turnList), self.winner)
        self.turnList.append(turns.turn)
        self.cardCount = self.cardCount + len(player.hand.cards) + len(player.hand.cards2) + len(dealer.hand.cards)
        player.restart()
        dealer.restart()
        if self.cardCount >= 40:
            deck.shuffle()
        self.winner = ""
        self.game()

class Turns():
    def __init__(self):
        self.turn = []

    def update(self, number, winner):
        temp = [[],[],[],[],[]]
        temp[0] = "Turn #" + str(number)
        temp[1] = player.name + "'s hand: " + str(player.hand.hand_info())
        temp[2] = "Dealer hand: " + str(dealer.hand.hand_info())
        temp[3] = "Winner: " + winner
        temp[4] = "Bankroll: " + str(player.bankroll)
        self.turn.append(temp)

    def __repr__(self):
        return self.turn

class Button():
    def __init__(self,msg, msgColor, x, y, w, h, ic, ac, func = None, parameter = None):
        self.msg,self.msgColor,self.x,self.y,self.w,self.h,self.ic,self.ac,self.function,self.parameter = msg, msgColor, x, y, w, h, ic, ac, func, parameter

    def text_objects(self, text, font,color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def hide(self):
        pygame.draw.rect(gameDisplay, green,(self.x,self.y,self.w,self.h))
        pygame.display.update()
        close()

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        clicked = False
        txtColor = self.msgColor
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(gameDisplay, self.ac,(self.x,self.y,self.w,self.h))
            txtColor = self.ic
            if click[0] == 1:
                clicked = True
                try:
                    time.sleep(.1)
                    self.function(self.parameter)
                except TypeError:
                    try:
                        self.function()
                    except TypeError:
                        return self.parameter

        else:
            pygame.draw.rect(gameDisplay, self.ic,(self.x,self.y,self.w,self.h))

        smallText = pygame.font.SysFont(None, 50)
        textSurf, textRect = self.text_objects(self.msg, smallText, txtColor)
        textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)))
        gameDisplay.blit(textSurf, textRect)
        pygame.display.update()
        close()
        return clicked

def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                import games
        
def load_out():
    global stop_loop
    stop_loop = True
    
class Name():
    def __init__(self):
        gameDisplay.fill(green)
        self.name = ""
        self.count = 0

    def Box(self):
        upper = False
        mm = 0
        blinker = ""
        while True:
            gameDisplay.fill(green)
            gameDisplay.blit(pygame.font.SysFont(None, 75).render("Enter your name", True, white,green), (200,350))
            pygame.draw.rect(gameDisplay, white,(210,410,380,75))
            pygame.draw.rect(gameDisplay, green,(220,420,360,55))
            gameDisplay.blit(pygame.font.SysFont(None, 50).render(self.name + blinker, True, white), (225,430))
            gameDisplay.blit(pygame.font.SysFont(None, 20).render("PLEASE: Keep name short enough to fit in the white box", True, blue), (10,780))
            mm += .75
            if mm > 20 and mm < 40:
                blinker = chr(ord("|"))
            elif mm > 40:
                mm = 0
            else:
                blinker = ""
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_RIGHT:
                        upper = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pygame.K_RETURN:
                        return self.name
                    else:
                        toAdd = chr(event.key)
                        if upper:
                            toAdd = toAdd.upper()
                        self.name = self.name + toAdd
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT:
                        upper = False
                if event.type == pygame.QUIT:
                    time.sleep(.2)
                    import games
                    pygame.quit()
                    quit()
            pygame.display.update()
            clock.tick(100)


def game_start():
    global name, gameDisplay, game, clock, turns
    gameDisplay = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Blackjack   |   Best Score: $" + str(highScore.best_score) + " by " + highScore.best_name)
    pygame.display.set_icon(pygame.image.load('aces.png'))
    pygame.display.update()
    clock = pygame.time.Clock()
    gameDisplay.fill(green)
    close()
    name = Name()
    name = name.Box()
    turns = Turns()
    game = Game()

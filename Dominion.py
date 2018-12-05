import random
from tkinter import *

class Player:

    def __init__(self, name):
        self.name = name
        self.deck = ['Estate'] * 3 + ['Copper'] * 7
        random.shuffle(self.deck)
        self.hand = []
        self.discardpile = []
        self.playarea = []
        self.buys = 1
        self.actions = 1
        self.money = 0

class Game:

    def startgame(self):

        # FORMAT FOR CARDS = [name, cost, supply, type, +cards, +buys, +actions, +money]
        self.supplyCards = [['Copper', 0, 46, 'treasure', 0, 0, 0, 1], ['Silver', 3, 40, 'treasure', 0, 0, 0, 2], ['Gold', 6, 30, 'treasure', 0, 0, 0, 3],
                            ['Estate', 2, 8, 'victory', 0, 0, 0, 0], ['Duchy', 5, 8, 'victory', 0, 0, 0, 0], ['Province', 8, 8, 'victory', 0, 0, 0, 0],
                            ['Village', 3, 10, 'action', 1, 0, 2, 0], ['Smithy', 4, 10, 'action', 3, 0, 0, 0], ['Market', 5, 10, 'action', 1, 1, 1, 1], ['Festival', 5, 10, 'action', 0, 1, 2, 2],
                            ['Laboratory', 5, 10, 'action', 2, 0, 1, 0]]
        self.gameOver = False
        self.turnEnd = False

        print("Game initialized")
    
        
    def newwindow(self):

        self.root = Tk(  )
        self.root.title("Dominion")

        self.Frame1 = Frame(self.root)
        self.Frame2 = Frame(self.root)

        self.Frame1.pack()
        self.Frame2.pack()


    def drawCard(self, amount):
        i = 0
        while i < amount:
            if len(Player1.deck) == 0:
                Player1.deck.extend(Player1.discardpile)
                random.shuffle(Player1.deck)
                Player1.discardpile = []
        
            Player1.hand.append(Player1.deck[0])
            Player1.deck.remove(Player1.deck[0])
            i += 1

    def cardFinder(self, cardname):
        for x in self.supplyCards:
            if x[0] == cardname: return x

    def endTurn(self):
        self.turnEnd = True
        self.reloadscreen()

    def cleanup(self):

        for x in Player1.hand:
            Player1.discardpile.append(x)
        Player1.hand = []

        for y in Player1.playarea:
            Player1.discardpile.append(y)
        Player1.playarea = []

        self.drawCard(5)

        Player1.actions = 1
        Player1.buys = 1
        Player1.money = 0

        self.turnEnd = False

        if len([i for i in self.supplyCards if i[2] == 0]) >= 3 or self.cardFinder('Province')[2] == 0:
            self.gameOver = True

        #       ********************
        #       **** BUY CARDS *****
        #       ********************

    def buyCard(self, userCommand):
        CardToBuy = self.cardFinder(userCommand)
        if Player1.buys == 0: 
            print( "You don't have any remaining buys" ) 
            self.reloadscreen()
        elif Player1.money < CardToBuy[1]: 
            print( "You don't have enough money to purchase that!" )
            self.reloadscreen()
        elif CardToBuy[2] == 0: 
            print( "That card's supply pile is empty!" )
            self.reloadscreen()
        else:
            Player1.discardpile.append(CardToBuy[0])
            Player1.money -= CardToBuy[1]
            Player1.buys -= 1
            updatedCard = CardToBuy
            updatedCard[2] -= 1
            self.supplyCards[self.supplyCards.index(CardToBuy)] = updatedCard
            self.reloadscreen()

            print( CardToBuy[0] + " bought")


    def playCard(self, userCommand):
        if userCommand == "All":
            moneyincrease = 0
            for x in Player1.hand:
                if self.cardFinder(x)[3] == 'treasure':
                    moneyincrease += self.cardFinder(x)[7]
                    Player1.playarea.append(self.cardFinder(x)[0])
            Player1.hand = [i for i in Player1.hand if i not in {'Copper', 'Silver', 'Gold'}]
            Player1.money += moneyincrease
        else:
            CardToPlay = self.cardFinder(userCommand)
            if Player1.actions == 0 and CardToPlay[3] == 'action': 
                print( "You don't have any remaining actions" ) 
                self.reloadscreen()
            elif Player1.actions > 0 and CardToPlay[3] == 'action':
                Player1.actions -= 1

            Player1.playarea.append(CardToPlay[0])
            Player1.hand.remove(CardToPlay[0])

            if CardToPlay[4] > 0: self.drawCard(CardToPlay[4]) and print(CardToPlay[4] + " cards drawn")
            Player1.buys += CardToPlay[5]
            Player1.actions += CardToPlay[6]
            Player1.money += CardToPlay[7]

            print( CardToPlay[0] + " played")

        self.reloadscreen()

        #       ********************
        #       *** FINAL SCORE ****
        #       ********************

    def pointTally(self):

        Player1.deck.extend(Player1.discardpile)
        Player1.deck.extend(Player1.hand)

        estateCount = len([i for i in Player1.deck if i == 'Estate'])
        duchyCount = len([i for i in Player1.deck if i == 'Duchy'])
        provinceCount = len([i for i in Player1.deck if i == 'Province'])
        finalScore = 1 * estateCount + 3 * duchyCount + 6 * provinceCount
        
        print("\nGame over, final score is: \n")
        print("Estates     : " + str(estateCount))
        print("Duchys      : " + str(duchyCount))
        print("Provinces   : " + str(provinceCount) + "\n")
        print("Final score : " + str(finalScore) + " victory points")

        #       ********************
        #       ***** DISPLAY ******
        #       ********************

    def reloadscreen(self):
        self.root.destroy()


    def display(self):
        
        Supply = Text(self.Frame1, height=15, width=40)

        Supply.insert(INSERT, "|    Card name  | Cost | Supply |\n")
        i = 1
        for x in self.supplyCards:
           if x[3] != 'action':
            Supply.insert(INSERT, "| " + str(i) + ". " + str(x[0]) + " " * (11 - len(x[0])) +
                    "| " + str(x[1]) + " $" + " " * (3 - len(str(x[1]))) +
                    "| " + str(x[2]) + " " * (6 - len(str(x[2]))) + " |\n")
            i += 1
        Supply.grid(row=0, column=0)

        Supply2 = Text(self.Frame1, height=15, width=40)

        Supply2.insert(INSERT, "|    Card name  | Cost | Supply |\n")
        i = 1
        for x in self.supplyCards:
          if x[3] == 'action':
            Supply2.insert(INSERT, "| " + str(i) + ". " + str(x[0]) + " " * (11 - len(x[0])) +
                    "| " + str(x[1]) + " $" + " " * (3 - len(str(x[1]))) +
                    "| " + str(x[2]) + " " * (6 - len(str(x[2]))) + " |\n")
            i += 1
        Supply2.grid(row=0, column=1)

        Hand = Text(self.Frame1, height=15, width=40)

        Hand.insert(INSERT, "Cards in hand:\n")
        i = 1
        for x in Player1.hand:
            Hand.insert(INSERT, str(i) + ". " + str(x) + "\n")
            i += 1

        Hand.grid(row=1, column=0)

        Status = Text(self.Frame1, height=15, width=40)

        Status.insert(INSERT, Player1.name + "'s current status:\n")
        Status.insert(INSERT, "  Money : " + str(Player1.money) + " $\n")
        Status.insert(INSERT, "   Buys : " + str(Player1.buys) + "\n")
        Status.insert(INSERT, "Actions : " + str(Player1.actions) + "\n\n")
        Status.insert(INSERT, "Cards in discard pile : " + str(len(Player1.discardpile)) + "\n")
        Status.insert(INSERT, "Cards in deck         : " + str(len(Player1.deck)))
        
        Status.grid(row=1, column=1)

        #       ********************
        #       ******* MENU *******
        #       ********************

        playTreasuresButton = Button ( self.Frame2, text="Play all treasures", command= lambda: self.playCard("All") ) 
        playTreasuresButton.grid(row=0, column=0, padx=20)

        playButton=  Menubutton ( self.Frame2, text="Play cards from hand" )
        playButton.grid(row=0, column=0)
        playButton.menu =  Menu ( playButton, tearoff = 0 )
        playButton["menu"] =  playButton.menu

        for x in Player1.hand:
            if x not in ['Estate', 'Duchy', 'Province']:
                playButton.menu.add_command ( label=self.cardFinder(x)[0] + " - " + self.cardFinder(x)[3], command= lambda i = x: self.playCard(i) )
        
        playButton.grid(row=0, column=1, padx=20)

        buyButton=  Menubutton ( self.Frame2, text="Buy cards from the supply" )
        buyButton.grid(row=0, column=1)
        buyButton.menu =  Menu ( buyButton, tearoff = 0 )
        buyButton["menu"] =  buyButton.menu

        if Player1.buys > 0:
            for x in self.supplyCards:
                buyButton.menu.add_command ( label=x[0] + " - " + str(x[1]) + " $", command= lambda i = x[0]: self.buyCard(i) )
        else:
            buyButton.menu.add_command ( label="You don't have any remaining buys!", command= self.reloadscreen )

        buyButton.grid(row=0, column=2, padx=20)

        EndturnButton=  Button ( self.Frame2, text="End turn", command= self.endTurn )
        EndturnButton.grid(row=0, column=3, padx=20)

        self.root.mainloop(  )


if __name__=="__main__":
    Dominion = Game()
    name = 'Player 1' #input("What's your name? : ")
    Player1 = Player(name)

    Dominion.startgame()
    Dominion.drawCard(5)

    while Dominion.gameOver == False:
        while Dominion.turnEnd == False:
            Dominion.newwindow()
            Dominion.display()
        Dominion.cleanup()

    Dominion.pointTally()
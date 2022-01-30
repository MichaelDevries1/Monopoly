import random
import math


def advancetogo():
    print('Advance to Go. (Collect $200) \n\n\n\n\n')


def buildLocation(cardType):
    if cardType == "Go":
        return Go(
            propType = "Go",
            cardName="Go",
            cardPayment=200
        )
    elif cardType == "buildable":
        return Buildable(
            pType="buildable",
            pName="Mediteranian Avenue",
            pCost=60,
            pRent=2,
            pRent1=10,
            pRent4=160,
            pRentHotel=250,
            pBuildingCost=50
        )

# Setting Variables
# Name of all locations on the board
name = {
    0: "Go",
    1: 'Mediterranean Avenue',
    2: 'Community Chest',
    3: 'Baltic Avenue',
    4: 'Income Tax',
    5: 'Reading Railroad',
    6: 'Oriental Avenue',
    7: 'Chance',
    8: 'Vermont Avenue',
    9: 'Connecticut Avenue',
    10: 'Just Visiting',
    11: 'St. Charles Place',
    12: 'Electric Company',
    13: 'States Avenue',
    14: 'Virginia Avenue',
    15: 'Pennsylvania Railroad',
    16: 'St. James Place',
    17: 'Community Chest',
    18: 'Tennessee Avenue',
    19: 'New York Avenue',
    20: 'Free Parking',
    21: 'Kentucky Avenue',
    22: 'Chance',
    23: 'Indiana Avenue',
    24: 'Illinois Avenue',
    25: 'B&O Railroad',
    26: 'Atlantic Avenue',
    27: 'Ventnor Avenue',
    28: 'Water Works',
    29: 'Marvin Gardens',
    30: 'Go To Jail',
    31: 'Pacific Avenue',
    32: 'North Carolina Avenue',
    33: 'Community Chest',
    34: 'Pennsylvania Avenue',
    35: 'Short Line',
    36: 'Chance',
    37: 'Park Place',
    38: 'Luxury Tax',
    39: 'Boardwalk',
    40: 'In Jail'
}
# All Chance cards
chance = {
    1: 'Advance to Boardwalk',
    2: 'Advance to Go',
    3: 'Advance to Illinois Avenue. If you pass Go, collect $200',
    4: 'Advance to St. Charles Place. If you pass Go, collect $200',
    5: 'Advance to the nearest railroad. If unowned, you may buy it from the Bank. If owned, pay owner twice the rental'
       'to which they are otherwise entitled.',
    6: 'Advance to the nearest railroad. If unowned, you may buy it from the Bank. If owned, pay owner twice the rental'
       'to which they are otherwise entitled.',
    7: 'Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner'
       'a total of ten times amount thrown.',
    8: 'Bank pays you dividend of $50',
    9: 'Get Out of Jail Free',
    10: 'Go back 3 spaces',
    11: 'Go to Jail. Go directly to Jail, do not pass Go, do not collect $200',
    12: 'Make general repairs on all your property. For each house pay $25. For each hotel pay $100.',
    13: 'Speeding fine $15',
    14: 'Take a trip to Reading Railroad. If you pass Go, collect $200',
    15: 'You have been elected Chairman of the Board. Pay each player $50',
    16: 'Your building loan matures. Collect $150'
}
# All Community Chest Cards
com_chest = {
    1: 'advancetogo()',
    2: 'Bank error in your favor. Collect $200',
    3: "Doctor's fee. Pay $50",
    4: 'From sale of stock you get $50',
    5: 'Get Out of Jail Free',
    6: 'Go to Jail. Go directly to Jail, do not pass Go, do not collect $200',
    7: 'Holiday fund matures. Receive $100',
    8: 'Income tax refund. Collect $20',
    9: 'It is your birthday. Collect $10 from every player.',
    10: 'Life insurance matures. Collect $100.',
    11: 'Pay hospital fees of $100',
    12: 'Pay school fees of $50',
    13: 'Receive $25 consultancy fee.',
    14: 'You are assessed for street repair. $40 per house. $115 per hotel.',
    15: 'You have won second prize in a beauty contest. Collect $10',
    16: 'You inherit $100.'
}
# Dice variables
dice1 = -1
dice2 = -1
double_count = 0
# Player Location on the board
location = 0
# Turn number this game
turn = 0
cardType = "Go"

while turn < 200:
    # Increase turn count and display
    turn += 1
    print("Turn #: ", turn)

    # Roll the 2 dice, add them together and display the results
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    print("Dice 1: ", dice1, " Dice 2: ", dice2, " Dice sum: ", dice_sum)

    # Monitor number of doubles rolled in a row
    if dice1 == dice2:
        double_count += 1
        print('Doubles thrown: ', double_count)
    else:
        double_count = 0

    # Figure out new location of player
    location += dice_sum
    # Check if player goes to jail or returns to Go naturally
    if double_count == 3 or location == 30:
        print('WENT TO JAIL \n\n\n')
        location = 40
    elif location > 39:
        location -= 40

    # Check if player landed on chance and draw card.
    if location == 7 or location == 22 or location == 36:
        draw_chance = chance[random.randint(1, len(chance))]
        print('Take a chance card! You drew: ', draw_chance, '\n\n\n')

    # Check if player landed on community chest and draw a card.
    if location == 2 or location == 17 or location == 33:
        draw_comm = eval(com_chest[1])
        # draw_comm = com_chest[random.randint(1, len(com_chest))]
        # print('Take a community chest card! You drew: ', draw_comm, '\n\n\n')

    # Display current location
    print('Location: ', name[location])
    print('')


class Go:
    type = ""
    name = ""
    payment = 0

    def __init__(self, propType, cardName, cardPayment):
        self.type = propType
        self.name = cardName
        self.payment = cardPayment

    def getName(self):
        return self.name

    def getPayment(self):
        return self.payment

    def getInfo(self):
        return [self.type, self.name, self.payment]


class Buildable:
    type = ''
    name = ''
    cost = ''
    rent0 = 0
    colorRent = 0
    rent1 = 0
    rent2 = 0
    rent3 = 0
    rent4 = 0
    rentHotel = 0
    buildingCost = 0
    mortgageValue = 0
    unmortgageCost = 0
    isMortgaged = False
    owner = ''
    level = 0

    def __init__(self, pType, pName, pCost, pRent, pRent1, pRent4, pRentHotel, pBuildingCost):
        self.type = pType
        self.name = pName
        self.cost = pCost
        self.rent0 = pRent
        self.colorRent = self.rent0 * 2
        self.rent1 = pRent1
        self.rent2 = self.rent1 * 3
        self.rent3 = self.rent1 * 9
        self.rent4 = pRent4
        self.rentHotel = pRentHotel
        self.buildingCost = pBuildingCost
        self.mortgageValue = self.cost / 2
        self.unmortgageCost = int(math.ceil(self.mortgageValue * 1.1))

    def setOwner(self, player):
        self.owner = player

    def setLevel(self, level):
        self.level = level

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def getOwner(self):
        return self.owner

    def getName(self):
        return self.name

    def getLevel(self):
        return self.level

    def getRents(self):
        return [self.rent0, self.colorRent, self.rent1, self.rent2, self.rent3, self.rent4, self.rentHotel]

    def getBuildingCost(self):
        return self.buildingCost

    def getMortgageValue(self):
        return self.mortgageValue

    def getUnmortgageCost(self):
        return self.unmortgageCost

    def getIsMortgaged(self):
        return self.isMortgaged

    def getInfo(self):
        return [self.type, self.name, self.rent0, self.colorRent, self.rent1, self.rent2, self.rent3, self.rent4,
                self.rentHotel, self.buildingCost, self.mortgageValue, self.unmortgageCost, self.isMortgaged,
                self.owner, self.level]


class Tax:
    type = ''
    name = ''
    tax = 0

    def __init__(self, pType, pName, pTax):
        self.type = pType
        self.name = pName
        self.tax = pTax

    def getName(self):
        return self.name

    def getTax(self):
        return self.tax

    def getInfo(self):
        return [self.type, self.name, self.tax]


class Railroad:
    type = ''
    name = ''
    cost = 0
    rent = 0
    rent2 = 0
    rent3 = 0
    rent4 = 0
    mortgageValue = 0
    unmortgageCost = 0
    isMortgaged = False
    owner = ''
    level = 0

    def __init__(self, pType, pName, pCost, pRent):
        self.type = pType
        self.name = pName
        self.cost = pCost
        self.rent1 = pRent
        self.rent2 = self.rent * 2
        self.rent3 = self.rent2 * 2
        self.rent4 = self.rent3 * 2
        self.mortgageValue = self.cost / 2
        self.unmortgageCost = int(math.ceil(self.mortgageValue * 1.1))

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def setOwner(self, newOwner):
        self.owner = newOwner

    def setLevel(self, newLevel):
        self.level = newLevel

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost

    def getRent1(self):
        return self.rent1

    def getRent2(self):
        return self.rent2

    def getRent3(self):
        return self.rent3

    def getRent4(self):
        return self.rent4

    def getRents(self):
        return [self.rent1, self.rent2, self.rent3, self.rent4]

    def getMortgageValue(self):
        return self.mortgageValue

    def getUnmortgageCost(self):
        return self.unmortgageCost

    def getIsMortgaged(self):
        return self.isMortgaged

    def getOwner(self):
        return self.owner

    def getLevel(self):
        return self.level

    def getInfo(self):
        return [self.type, self.name, self.cost, self.rent1, self.rent2, self.rent3, self.rent4, self.mortgageValue,
                self.unmortgageCost, self.isMortgaged, self.owner, self.level]


class NoAction:
    type = ''
    name = ''

    def __init__(self, pType, pName):
        self.type = pType
        self.name = pName

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getInfo(self):
        return [self.type, self.name]


class Utility:
    type = ''
    name = ''
    cost = 0
    rent1 = 4
    rent2 = 10
    mortgageValue = 0
    unmortgageCost = 0
    isMortgaged = False
    owner = ''
    level = 0

    def __init__(self, pType, pName, pCost):
        self.type = pType
        self.name = pName
        self.cost = pCost
        self.mortgageValue = self.cost / 2
        self.unmortgageCost = int(math.ceil(self.mortgageValue * 1.1))

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def setOwner(self, newOwner):
        self.owner = newOwner

    def setLevel(self, newLevel):
        self.level = newLevel

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost

    def getRent1(self):
        return self.rent1

    def getRent2(self):
        return self.rent2

    def getRents(self):
        return [self.rent1, self.rent2]

    def getMortgageValue(self):
        return self.mortgageValue

    def getUnmortgageCost(self):
        return self.unmortgageCost

    def getIsMortgaged(self):
        return self.isMortgaged

    def getOwner(self):
        return self.owner

    def getLevel(self):
        return self.level

    def getInfo(self):
        return [self.type, self.name, self.cost, self.rent1, self.rent2, self.mortgageValue, self.unmortgageCost,
                self.isMortgaged, self.owner, self.level]

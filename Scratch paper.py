import random
import math
import json


class SimpleLocation:
    # The basic location object. It allows for the retrieval of the name and type of location.
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


class Go(SimpleLocation):
    # The Go location object. Requires the SimpleLocation object. Used to retrieve information for "Go"
    payment = 200

    def __init__(self, propType, cardName):
        super().__init__(propType, cardName)

    def getPayment(self):
        return self.payment

    def getInfo(self):
        return [self.type, self.name, self.payment]


class Property(SimpleLocation):
    # Second level of object for any location that can be owned. This includes buildables, railroads, and utilities.
    cost = ''               # Cost of purchasing the property
    mortgageValue = 0       # How much player gets if property is mortgaged
    unmortgageCost = 0      # How much player pays to unmortgage the property
    isMortgaged = False     # Is the property currently mortgaged?
    owner = ''              # Player that owns the property.

    def __init__(self, pType, pName, pCost):
        super().__init__(pType, pName)
        self.type = pType
        self.name = pName
        self.cost = pCost
        self.mortgageValue = self.cost / 2
        self.unmortgageCost = int(math.ceil(self.mortgageValue * 1.1))

    def setOwner(self, player):
        self.owner = player

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def getOwner(self):
        return self.owner

    def getMortgageValue(self):
        return self.mortgageValue

    def getUnmortgageCost(self):
        return self.unmortgageCost

    def getIsMortgaged(self):
        return self.isMortgaged


class Buildable(Property):
    # Third level of objects for properties that can have houses and hotels built upon them.
    color = ''          # The color group of the property.
    colorRent = 0       # The amount of rent collected once all of that color is collected
    rent0 = 0           # The amount of rent collected with 0 houses
    rent1 = 0           # The amount of rent collected with 1 house
    rent2 = 0           # The amount of rent collected with 2 houses
    rent3 = 0           # The amount of rent collected with 3 houses
    rent4 = 0           # The amount of rent collected with 4 houses
    rentHotel = 0       # The amount of rent collected with a hotel
    buildingCost = 0    # The cost for building one structure (house/hotel)
    level = 0           # The current number of houses/hotel on property. 0=0 houses, 1=1 house...4=4 houses, 5=hotel.

    def __init__(self, pType, pName, pCost, pColor, pRent, pRent1, pRent4, pRentHotel, pBuildingCost):
        super().__init__(pType, pName, pCost)
        self.color = pColor
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

    def setLevel(self, level):
        self.level = level

    def getColor(self):
        return self.color

    def getLevel(self):
        return self.level

    def getRents(self):
        return [self.rent0, self.colorRent, self.rent1, self.rent2, self.rent3, self.rent4, self.rentHotel]

    def getBuildingCost(self):
        return self.buildingCost

    def getInfo(self):
        return [self.type, self.name, self.color, self.rent0, self.colorRent, self.rent1, self.rent2, self.rent3,
                self.rent4, self.rentHotel, self.buildingCost, self.mortgageValue, self.unmortgageCost,
                self.isMortgaged, self.owner, self.level]


class Tax(SimpleLocation):
    # Tax location objects. This includes income and luxury tax locations.
    tax = 0         # The amount a player has to play

    def __init__(self, pType, pName, pTax):
        super().__init__(pType, pName)
        self.tax = pTax

    def getTax(self):
        return self.tax

    def getInfo(self):
        return [self.type, self.name, self.tax]


class Railroad(Property):
    # Third level of objects for railroad properties.
    rent1 = 25      # rent received when a player lands on 1 owned railroad
    rent2 = 50      # rent received when a player lands on 2 owned railroads
    rent3 = 100     # rent received when a player lands on 3 owned railroads
    rent4 = 200     # rent received when a player lands on 4 owned railroads
    level = 0       # Current number of railroads owned by owner. 0=none, 1=1 railroad.. 4=all railroads.

    def __init__(self, pType, pName, pCost):
        super().__init__(pType, pName, pCost)

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


class Utility(Property):
    # Third level of objects for utility properties.
    rent1 = 4       # dice roll multiple received when a player lands on 1 owned utility
    rent2 = 10      # dice roll multiple received when a player lands on 2 owned utilities
    level = 0       # Current number of utilities owned by owner. 0=none, 1=1 utility, or 2=2 utilities

    def __init__(self, pType, pName, pCost):
        super().__init__(pType, pName, pCost)
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


class Player:
    name = 'Player 1'       # Default name for a single player.
    wallet = 0              # Default amount in players wallet. (usually overwritten with $1500 upon creation)
    inJail = False          # Determines if player is currently in Jail or not
    # Get out of jail free cards held by player. One for chance and community chest draws.
    goojfChance = False
    goojfComm = False
    ownedProperties = []    # List of all owned property objects

    def __init__(self, pName):
        self.name = pName
        self.wallet = 1500

    def setWallet(self, amount):
        self.wallet += amount

    def addNewProperty(self, newProperty):
        self.ownedProperties.append(newProperty)

    def toggleInJail(self):
        self.inJail = not self.inJail

    def toggleGOoJFChance(self):
        self.goojfChance = not self.goojfChance

    def toggleGOoJFComm(self):
        self.goojfComm = not self.goojfComm

    def removeProperty(self, subProperty):
        self.ownedProperties.remove(subProperty)

    def getName(self):
        return self.name

    def getWallet(self):
        return self.wallet

    def getInJail(self):
        return self.inJail

    def getGOoJFChance(self):
        return self.goojfChance

    def getGOoJFComm(self):
        return self.goojfComm

    def getOwnedProperties(self):
        return self.ownedProperties

    def getInfo(self):
        return [self.name, self.wallet, self.inJail, self.ownedProperties]


def buildLocation():
    locationNames = {}
    locationFile = open('C:\\Users\\compu\\Dropbox\\selfStudy\\Monopoly\\Monopoly\\Locations.json')
    data = json.load(locationFile)
    x = 0

    for i in data['locations']:
        cardType = data['locations'][x]['proptype']
        if cardType == "go":
            locationNames[x] = Go(
                propType='go',
                cardName=data['locations'][x]['name'],
            )
        elif cardType == "buildable":
            locationNames[x] = Buildable(
                pType='buildable',
                pName=data['locations'][x]['name'],
                pCost=data['locations'][x]['cost'],
                pRent=data['locations'][x]['rent0'],
                pRent1=data['locations'][x]['rent1'],
                pRent4=data['locations'][x]['rent4'],
                pRentHotel=data['locations'][x]['rentHotel'],
                pBuildingCost=data['locations'][x]['buildingCost']
            )
        elif cardType == 'tax':
            locationNames[x] = Tax(
                pType='tax',
                pName=data['locations'][x]['name'],
                pTax=data['locations'][x]['tax']
            )
        elif cardType == 'railroad':
            locationNames[x] = Railroad(
                pType='railroad',
                pName=data['locations'][x]['name'],
                pCost=data['locations'][x]['cost']
            )
        elif cardType == 'simpleLocation':
            locationNames[x] = SimpleLocation(
                pType='simpleLocation',
                pName=data['locations'][x]['name']
            )
        elif cardType == 'utility':
            locationNames[x] = Utility(
                pType='utility',
                pName=data['locations'][x]['name'],
                pCost=data['locations'][x]['cost']
            )
        # print(str(x), ': ', locationNames.get(x).getName())
        x += 1
    locationFile.close()
    return locationNames


def playerSetup(playerName):
    return Player(playerName)


def newGame():
    # Resets the basic variables to starting state. Also allows creation of players.
    global bankCash
    global bankHouses
    global bankHotels
    global LocationName
    bankCash = 28580    # Bank will always start with $28580 in cash.
    bankHouses = 32     # Bank will always start with 32 available houses.
    bankHotels = 12     # Bank will always start with 12 available hotels.
    LocationName = buildLocation()  # The dictionary of all location objects


# The start of the main program at this point 2/3/22
# Setting initial global variables
maxBankCash = 28580     # Maximum amount of cash used in the game
maxHouses = 0           # Maximum amount of houses used in the game
maxHotels = 0           # Maximum amount of hotels used in the game
bankCash = 0            # Current amount of cash in the bank
bankHouses = 0          # Current amount of available houses
bankHotels = 0          # Current amount of available hotels
locationName = {}       # Dictionary of all location objects for the board

newGame()               # Reset the game to its basic beginning state

'''
def advancetogo():
    print('Advance to Go. (Collect $200) \n\n\n\n\n')

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
'''




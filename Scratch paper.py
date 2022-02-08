import random
import json
import math
import io
from Monopoly import player as Player


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
    cost = ''  # Cost of purchasing the property
    mortgageValue = 0  # How much player gets if property is mortgaged
    unmortgageCost = 0  # How much player pays to unmortgage the property
    isMortgaged = False  # Is the property currently mortgaged?
    owner = ''  # Player that owns the property.

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
    color = ''  # The color group of the property.
    colorRent = 0  # The amount of rent collected once all of that color is collected
    rent0 = 0  # The amount of rent collected with 0 houses
    rent1 = 0  # The amount of rent collected with 1 house
    rent2 = 0  # The amount of rent collected with 2 houses
    rent3 = 0  # The amount of rent collected with 3 houses
    rent4 = 0  # The amount of rent collected with 4 houses
    rentHotel = 0  # The amount of rent collected with a hotel
    buildingCost = 0  # The cost for building one structure (house/hotel)
    level = 0  # The current number of houses/hotel on property. 0=0 houses, 1=colorRent, 2=1 house

    #                     ...5=4 houses, 6=hotel.

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
    tax = 0  # The amount a player has to play

    def __init__(self, pType, pName, pTax):
        super().__init__(pType, pName)
        self.tax = pTax

    def getTax(self):
        return self.tax

    def getInfo(self):
        return [self.type, self.name, self.tax]


class Railroad(Property):
    # Third level of objects for railroad properties.
    rent1 = 25  # rent received when a player lands on 1 owned railroad
    rent2 = 50  # rent received when a player lands on 2 owned railroads
    rent3 = 100  # rent received when a player lands on 3 owned railroads
    rent4 = 200  # rent received when a player lands on 4 owned railroads
    level = 0  # Current number of railroads owned by owner. 0=none, 1=1 railroad.. 4=all railroads.

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
    rent1 = 4  # dice roll multiple received when a player lands on 1 owned utility
    rent2 = 10  # dice roll multiple received when a player lands on 2 owned utilities
    level = 0  # Current number of utilities owned by owner. 0=none, 1=1 utility, or 2=2 utilities

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


def newGame():
    # Resets the basic variables to starting state. Also allows creation of players.
    global bankCash
    global bankHouses
    global bankHotels
    global LocationName
    bankCash = 28580  # Bank will always start with $28580 in cash.
    bankHouses = 32  # Bank will always start with 32 available houses.
    bankHotels = 12  # Bank will always start with 12 available hotels.
    LocationName = buildLocation()  # The dictionary of all location objects


def bankPayRequest(amount):
    global bankCash  # Check the amount of cash in the bank
    if bankCash > amount:  # check if the bank has more than the requested amount
        bankCash -= amount  # subtract the amount from the bank
        return amount  # return how much player will receive
    else:
        print('The bank doens\'t currently have that much. You get whats left which is $', bankCash)
        remainder = bankCash  # set how much the player will actually receive
        bankCash = 0  # set the bank cash to $0
        return remainder  # return how much player will receive


# START OF CARD ACTIONS
def advance(player, location, goBack):
    if goBack is True:
        player.setGivenPosition(player.position + location)
    if player.position > location:
        player.setGivenPosition(location)
        payamount = bankPayRequest(200)
        player.setWallet(payamount)
    else:
        player.setGivenPosition(location)


def collect(player, amount):
    payamount = bankPayRequest(amount)
    player.setWallet(payamount)


def repairs(player, houseCost, hotelCost):
    numHomes = 0  # number of homes player owns
    numHotels = 0  # number of hotels player owns
    propertyCount = player.getOwnedProperties()  # get the list of locations player owns
    # count the number of homes and hotels on each property
    for i in propertyCount:
        types = locationName[i].getType()  # get the type of property
        if types is "buildable":
            level = locationName[i].getLevel()  # get the level of property
            if level is 6:  # check for hotel
                numHotels += 1
            elif 1 < level < 6:  # check number of homes
                numHomes = numHomes + level - 1
    # check to see if player can pay amount
    player.playerPayBankRequest(player, (numHomes * houseCost + numHotels * hotelCost))


def railroad(player):
    print('')  # todo: add railroad chance card functionality


def utility():
    print('')  # todo: add utility chance card functionality


def birthday(player, playerArray, amount):
    print('This is for birthday collection from all players')  # todo: add birthday com chest card functionality


def chairman(player, playerArray, amount):
    print('This is for being elected chairman')  # todo: add chairman chance card functionality


curPlayer = Player() # TODO: TEST VARIABLE


# START OF COMMUNITY CHEST CARD ACTIONS
# TODO: change name of this function as it works with both decks
def community_chest_cards(player, action, message, amount1=0, amount2=0, playerArray=[], newSpace=-1, goBack=False):
    print(message)
    io.log_event(player + ", " + message)

    if action is 'advance':
        advance(player, newSpace, goBack)
    if action is 'collect':
        collect(player, amount1)
    elif action is 'pay':
        player.playerPayBankRequest(player, amount1)
    elif action is 'gotojail':
        player.setGoToJail()
    elif action is 'getoutofjailfreecomm':
        player.toggleGOoJFComm()
    elif action is 'getoutofjailfreecchance':
        player.toggleGOoJFChance()
    elif action is 'railroad':
        # TODO: This is where you calculate the closest forward moving railroad and advance to it, collecting 200 if necessary, and multiply by 2
    elif action is 'utility':
        # TODO: This is where you calculate the closest forward moving utility and advance to it, collecting 200 if necessary, and multiply by 10
    elif action is 'repairs':
        repairs(player, amount1, amount2)
    elif action is 'birthday':
        birthday(player, playerArray, amount1)
    elif action is 'chairman':
        chairman(player, playerArray, amount1)



# The start of the main program at this point 2/3/22
# Setting initial global variables
maxBankCash = 28580  # Maximum amount of cash used in the game
maxHouses = 0  # Maximum amount of houses used in the game
maxHotels = 0  # Maximum amount of hotels used in the game
bankCash = 0  # Current amount of cash in the bank
bankHouses = 0  # Current amount of available houses
bankHotels = 0  # Current amount of available hotels
locationName = {}  # Dictionary of all location objects for the board
# Dice variables
dice1 = -1
dice2 = -1
double_count = 0  # Count of how many doubles a player has received in a row
location = 0  # Player Location on the board
turn = 0  # Turn number this game
# All Chance cards
chance = {
    1: 'community_chest_cards(curPlayer, "advance", "Advance to Boardwalk", newSpace=39)',
    2: 'community_chest_cards(curPlayer, "advance", "Advance to Go", newSpace=0)',
    3: 'community_chest_cards(curPlayer, "advance", "Advance to Illinois Avenue. If you pass Go, collect $200", '
       'newSpace=24)',
    4: 'community_chest_cards(curPlayer, "advance", "Advance to St. Charles Place. If you pass Go, collect $200", '
       'newSpace=11)',
    5: 'community_chest_cards(curPlayer, "railroad", "Advance to the nearest railroad. If unowned, you may buy it from '
       'the Bank. If owned, pay owner twice the rental to which they are otherwise entitled.")',
    6: 'community_chest_cards(curPlayer, "railroad", "Advance to the nearest railroad. If unowned, you may buy it from '
       'the Bank. If owned, pay owner twice the rental to which they are otherwise entitled.")',
    7: 'community_chest_cards(curPlayer, "utility", "Advance token to nearest Utility. If unowned, you may buy it from '
       'the Bank. If owned, throw dice and pay owner a total of ten times amount thrown.")',
    8: 'community_chest_cards(curPlayer, "collect", "Bank pays you dividend of $50", amount1=50)',
    9: 'community_chest_cards(curPlayer, "getoutofjailfreecchance", "Get Out of Jail Free")',
    10: 'community_chest_cards(curPlayer, "advance", "Go back 3 spaces.", newSpace=(curPlayer.getPosition() - 3), '
        'goBack=True)',
    11: 'community_chest_cards(curPlayer, "gotojail", "Go to Jail. Go directly to Jail, do not pass Go, do not collect '
        '$200")',
    12: 'community_chest_cards(curPlayer, "repairs", "Make general repairs on all your property. For each house pay '
        '$25. For each hotel pay $100.", amount1=25, amount2=100)',
    13: 'community_chest_cards(curPlayer, "pay", "Speeding fine. Pay $15", amount1=15)',
    14: 'community_chest_cards(curPlayer, "advance", "Take a trip to Reading Railroad. If you pass Go, collect $200", '
        'newSpace=5)',
    15: 'community_chest_cards(curPlayer, "chairman", "You have been elected Chairman of the Board. Pay each player '
        '$50", amount1=50)',
    16: 'community_chest_cards(curPlayer, "collect", "Your building loan matures. Collect $150", amount1=150)'
}
# All Community Chest Cards
com_chest = {
    1: 'community_chest_cards(curPlayer, "advance", "Advance to Go")',
    2: 'community_chest_cards(curPlayer, "collect", "Bank error in your favor. Collect $200", amount1=200)',
    3: 'community_chest_cards(curPlayer, "pay", "Doctor\'s fee. Pay $50", amount1=50)',
    4: 'community_chest_cards(curPlayer, "collect", "From sale of stock you get $50", amount1=50)',
    5: 'community_chest_cards(curPlayer, "gotojail", "Go to Jail. Go directly to Jail, do not pass Go, do not '
       'collect $200", newSpace=40)',
    6: 'community_chest_cards(curPlayer, "getoutofjailfreecomm", "Get Out of Jail Free")',
    7: 'community_chest_cards(curPlayer, "collect", "Holiday fund matures. Receive $100", amount1=100)',
    8: 'community_chest_cards(curPlayer, "collect", "Income tax refund. Collect $20", amount1=20)',
    9: 'community_chest_cards(curPlayer, "birtday", "It is your birthday. Collect $10 from every player.",'
       ' amount1=10, playerArray=playerList)',
    10: 'community_chest_cards(curPlayer, "collect", "Life insurance matures. Collect $100.", amount1=100)',
    11: 'community_chest_cards(curPlayer, "pay", "Pay hospital fees of $100", amount1=100)',
    12: 'community_chest_cards(curPlayer, "pay", "Pay school fees of $50", amount1=50)',
    13: 'community_chest_cards(curPlayer, "collect", "Receive $25 consultancy fee.", amount1=25)',
    14: 'community_chest_cards(curPlayer, "repairs", "You are assessed for street repair. $40 per house. $115 per '
        'hotel.", amount1=40, amount2=115)',
    15: 'community_chest_cards(curPlayer, "collect", "You have won second prize in a beauty contest. Collect $10", '
        'amount1=10)',
    16: 'community_chest_cards(curPlayer, "collect", "You inherit $100.", amount1=100)'
}

newGame()  # Reset the game to its basic beginning state
'''
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

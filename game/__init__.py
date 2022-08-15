import random
import json
from game.io import Logging
from game.SimpleLocation import SimpleLocation
from game.Go import Go
from game.Buildable import Buildable
from game.Railroad import Railroad
from game.Tax import Tax
from game.Utility import Utility
from game.player import Player


class Monopoly:
    # Setting initial global variables
    jsonFile = 'game/Locations.json'
    data = ''
    maxBankCash = 28580  # Maximum amount of cash used in the game
    maxHouses = 0  # Maximum amount of houses used in the game
    maxHotels = 0  # Maximum amount of hotels used in the game
    bankCash = 0  # Current amount of cash in the bank
    bankHouses = 0  # Current amount of available houses
    bankHotels = 0  # Current amount of available hotels
    locationName = {}  # Dictionary of all location objects for the board
    playerList = []  # list of all players
    # Dice variables
    rolls = [-1, -1]
    double_count = 0  # Count of how many doubles a player has received in a row
    location = 0  # Player Location on the board
    turn = 0  # Turn number this game
    # All Chance cards
    chance = {
        1: 'draw_cards(curPlayer, "advance", "Advance to Boardwalk", new_space=39)',
        2: 'draw_cards(curPlayer, "advance", "Advance to Go", new_space=0)',
        3: 'draw_cards(curPlayer, "advance", "Advance to Illinois Avenue. If you pass Go, collect $200", new_space=24)',
        4: 'draw_cards(curPlayer, "advance", "Advance to St. Charles Place. If you pass Go, collect $200", '
           'new_space=11)',
        5: 'draw_cards(curPlayer, "railroad", "Advance to the nearest railroad. If unowned, you may buy it from the '
           'Bank. If owned, pay owner twice the rental to which they are otherwise entitled.")',
        6: 'draw_cards(curPlayer, "railroad", "Advance to the nearest railroad. If unowned, you may buy it from the '
           'Bank. If owned, pay owner twice the rental to which they are otherwise entitled.")',
        7: 'draw_cards(curPlayer, "utility", "Advance token to nearest Utility. If unowned, you may buy it from the '
           'Bank. If owned, throw dice and pay owner a total of ten times amount thrown.")',
        8: 'draw_cards(curPlayer, "collect", "Bank pays you dividend of $50", amount1=50)',
        9: 'draw_cards(curPlayer, "getoutofjailfreecchance", "Get Out of Jail Free")',
        10: 'draw_cards(curPlayer, "advance", "Go back 3 spaces.", new_space=(curPlayer.getPosition() - 3), '
            'go_back=True)',
        11: 'draw_cards(curPlayer, "gotojail", "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200")',
        12: 'draw_cards(curPlayer, "repairs", "Make general repairs on all your property. For each house pay $25. '
            'For each'
            ' hotel pay $100.", amount1=25, amount2=100)',
        13: 'draw_cards(curPlayer, "pay", "Speeding fine. Pay $15", amount1=15)',
        14: 'draw_cards(curPlayer, "advance", "Take a trip to Reading Railroad. If you pass Go, collect $200", '
            'new_space=5)',
        15: 'draw_cards(curPlayer, "chairman", "You have been elected Chairman of the Board. Pay each player $50", '
            'amount1=50, player_array=playerList)',
        16: 'draw_cards(curPlayer, "collect", "Your building loan matures. Collect $150", amount1=150)'
    }
    # All Community Chest Cards
    com_chest = {
        1: 'draw_cards(curPlayer, "advance", "Advance to Go")',
        2: 'draw_cards(curPlayer, "collect", "Bank error in your favor. Collect $200", amount1=200)',
        3: 'draw_cards(curPlayer, "pay", "Doctor\'s fee. Pay $50", amount1=50)',
        4: 'draw_cards(curPlayer, "collect", "From sale of stock you get $50", amount1=50)',
        5: 'draw_cards(curPlayer, "gotojail", "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200")',
        6: 'draw_cards(curPlayer, "getoutofjailfreecomm", "Get Out of Jail Free")',
        7: 'draw_cards(curPlayer, "collect", "Holiday fund matures. Receive $100", amount1=100)',
        8: 'draw_cards(curPlayer, "collect", "Income tax refund. Collect $20", amount1=20)',
        9: 'draw_cards(curPlayer, "birtday", "It is your birthday. Collect $10 from every player.", amount1=10, '
           'player_array=playerList)',
        10: 'draw_cards(curPlayer, "collect", "Life insurance matures. Collect $100.", amount1=100)',
        11: 'draw_cards(curPlayer, "pay", "Pay hospital fees of $100", amount1=100)',
        12: 'draw_cards(curPlayer, "pay", "Pay school fees of $50", amount1=50)',
        13: 'draw_cards(curPlayer, "collect", "Receive $25 consultancy fee.", amount1=25)',
        14: 'draw_cards(curPlayer, "repairs", "You are assessed for street repair. $40 per house. $115 per hotel.", '
            'amount1=40, amount2=115)',
        15: 'draw_cards(curPlayer, "collect", "You have won second prize in a beauty contest. Collect $10", '
            'amount1=10)',
        16: 'draw_cards(curPlayer, "collect", "You inherit $100.", amount1=100)'
    }

    @staticmethod
    def readJSON(jsonfile):
        if jsonfile is not '':
            location_file = open(jsonfile)
        else:
            location_file = open('game/Locations.json')
        data = json.load(location_file)
        return data

    @staticmethod
    def newPlayer():
        new_name = input('What is your name?')
        return Player(new_name)

    # todo: create new list of all color sets.
    def buildTheBoard(self, fileName):
        location_names = {}
        data = self.readJSON(fileName)
        x = 0

        for i in data['locations']:
            card_type = data['locations'][x]['proptype']
            if card_type == "go":
                location_names[x] = Go(
                    prop_type='go',
                    card_name=data['locations'][x]['name'],
                )
            elif card_type == "buildable":
                location_names[x] = Buildable(
                    pType='buildable',
                    pName=data['locations'][x]['name'],
                    pCost=data['locations'][x]['cost'],
                    pColor=data['locations'][x]['color'],
                    pRent=data['locations'][x]['rent0'],
                    pRent1=data['locations'][x]['rent1'],
                    pRent4=data['locations'][x]['rent4'],
                    pRentHotel=data['locations'][x]['rentHotel'],
                    pBuildingCost=data['locations'][x]['buildingCost']
                )
            elif card_type == 'tax':
                location_names[x] = Tax(
                    pType='tax',
                    pName=data['locations'][x]['name'],
                    pTax=data['locations'][x]['tax']
                )
            elif card_type == 'railroad':
                location_names[x] = Railroad(
                    pType='railroad',
                    pName=data['locations'][x]['name'],
                    pCost=data['locations'][x]['cost']
                )
            elif card_type == 'simpleLocation':
                location_names[x] = SimpleLocation(
                    p_type='simpleLocation',
                    p_name=data['locations'][x]['name']
                )
            elif card_type == 'utility':
                location_names[x] = Utility(
                    pType='utility',
                    pName=data['locations'][x]['name'],
                    pCost=data['locations'][x]['cost']
                )
            # print(str(x), ': ', location_names.get(x).getName())
            x += 1
        data.close()
        return location_names
    
    def newPlayerList(self, player_list):
        num_players = int(input('How many players are playing?'))
        while num_players < 1 or num_players > 4:
            num_players = int(input('Invalid number of players! Please choose a number between 1 and 4 players.'))
        for i in range(num_players):
            player_list[i - 1] = self.newPlayer()
        return player_list

    def newGame(self):
        # Resets the basic variables to starting state. Also allows creation of players.
        global bankCash
        global bankHouses
        global bankHotels
        global LocationName
        global jasonFile
        bankCash = 28580  # Bank will always start with $28580 in cash.
        bankHouses = 32  # Bank will always start with 32 available houses.
        bankHotels = 12  # Bank will always start with 12 available hotels.
        LocationName = self.buildTheBoard(jasonFile)  # The dictionary of all location objects

    @staticmethod
    def turnDiceRoll(rolls):
        # returns 2 dice rolls in a list
        rolls[1] = random.randint(1, 6)
        rolls[2] = random.randint(1, 6)
        return rolls

    @staticmethod
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

    def collectFromBank(self, cur_player, amount):
        pay_amount = self.bankPayRequest(amount)
        cur_player.setWallet(pay_amount)
        
    # START OF CARD ACTIONS
    def advance(self, cur_player, new_location, go_back):  # todo: firgure out where the action occurs upon reaching this new location (ie. paying rent)
        if go_back is True:  # Check if the player has to go back 3 spaces
            cur_player.setGivenPosition(cur_player.position + new_location)  # Move player back 3 spaces.
        if cur_player.position > new_location:  # Check to see if the player has to go around the board, passing go
            cur_player.setGivenPosition(new_location)  # place player at new location
            self.collectFromBank(cur_player, 200)  # Advancing past Go
        else:
            cur_player.setGivenPosition(new_location)  # place player at new location

    def repairs(self, cur_player, house_cost, hotel_cost):
        num_homes = 0  # number of homes player owns
        num_hotels = 0  # number of hotels player owns
        property_count = cur_player.getOwnedProperties()  # get the list of locations player owns
        # count the number of homes and hotels on each property
        for i in property_count:
            types = self.locationName[i].getType()  # get the type of property
            if types is "buildable":
                level = self.locationName[i].getLevel()  # get the level of property
                if level is 6:  # check for hotel
                    num_hotels += 1
                elif 1 < level < 6:  # check number of homes
                    num_homes = num_homes + level - 1
        # check to see if player can pay amount
        cur_player.playerPayRequest(cur_player, (num_homes * house_cost + num_hotels * hotel_cost))

    def modifiedRentUtilRail(self, cur_player, player_list, modifier):
        if self.locationName[cur_player.position].owner is not cur_player.getName and \
                self.locationName[cur_player.position].owner is not "":  # check ownership of property
            rent_level = self.locationName[cur_player.position].getLevel()
            rent_amount = self.locationName[cur_player.position].getRents()[rent_level - 1] * modifier
            cur_player.playerPayRequest(rent_amount)
            for receiving_player in player_list:
                if self.locationName[cur_player.position].owner is receiving_player.getName:
                    receiving_player.setWallet(rent_amount)
        else:
            # todo: find out if the player has enough money for the property.
            if cur_player.canPurchace(self.locationName[cur_player.position].getCost):
                # todo: make pop up asking if player wishes to purchase the property
                pass
            else:
                # todo: if the player doesn't have enough money or doesn't want the property, send it to auction
                pass

    def railroad(self, cur_player, player_list):
        if cur_player.position == 7:  # chance location between the blue set
            cur_player.setGivenPosition(15)  # set new location to Pennsylvania Railroad
        elif cur_player.position == 22:  # chance location between the red set
            cur_player.setGivenPosition(25)  # set new location to B&O Railroad
        elif cur_player.position == 36:  # chance location before park place
            cur_player.setGivenPosition(5)  # set new location to Reading Railroad, passing go
            self.collectFromBank(cur_player, 200)  # collect 200 for passing go
        # todo: Make a section for purchasing the property if it isn't owned.
        # todo: check if next block of code can be pulled into another function
        self.modifiedRentUtilRail(cur_player, player_list, 2)

    def utility(self, cur_player, player_list):
        if cur_player.position == 7:  # chance location between the blue set
            cur_player.setGivenPosition(12)  # set new location to Electric Company
        elif cur_player.position == 22:  # chance location between the red set
            cur_player.setGivenPosition(28)  # set new location to Water Works
        elif cur_player.position == 36:  # chance location before park place
            cur_player.setGivenPosition(12)  # set new location to Electric Company
            self.collectFromBank(cur_player, 200)  # collect 200 for passing go
        # todo: Make a section for purchasing the property if it isn't owned.
        # todo: check if next block of code can be pulled into another function
        self.modifiedRentUtilRail(cur_player, player_list, 10)

    def birthday(self, cur_player, playerArray, amount):
        print('This is for birthday collection from all players')  # todo: add birthday com chest card functionality
        num_players = len(playerArray) - 1

    def chairman(self, cur_player, playerArray, amount):
        print('This is for being elected chairman')  # todo: add chairman chance card functionality

    # START OF COMMUNITY CHEST CARD ACTIONS
    # TODO: change name of this function as it works with both decks
    def draw_cards(self, cur_player, action, message, amount1=0, amount2=0, player_array=[], new_space=-1,
                   go_back=False):
        print(message)
        io.log_event(cur_player + ", " + message)

        if action is 'advance':
            self.advance(cur_player, new_space, go_back)
        if action is 'collect':
            self.collectFromBank(cur_player, amount1)
        elif action is 'pay':
            cur_player.playerPayRequest(cur_player, amount1)
        elif action is 'gotojail':
            cur_player.setGoToJail()
        elif action is 'getoutofjailfreecomm':
            cur_player.toggleGOoJFComm()
        elif action is 'getoutofjailfreecchance':
            cur_player.toggleGOoJFChance()
        elif action is 'railroad':
            self.railroad(cur_player, player_array)
        elif action is 'utility':
            self.utility(cur_player)  # TODO: This is where you calculate the closest forward moving utility and advance to it,
            # collecting 200 if necessary, and multiply by 10
        elif action is 'repairs':
            self.repairs(cur_player, amount1, amount2)
        elif action is 'birthday':
            self.birthday(cur_player, player_array, amount1)
        elif action is 'chairman':
            self.chairman(cur_player, player_array, amount1)


    # The start of the main program at this point 2/3/22
    # newGame()  # Reset the game to its basic beginning state
    '''
    while turn < 200:
        # Increase turn count and display
        turn += 1
        print("Turn #: ", turn)
    
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

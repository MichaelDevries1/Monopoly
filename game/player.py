class Player:
    name = 'Player 1'  # Default name for a single player.
    wallet = 0  # Default amount in players wallet. (usually overwritten with $1500 upon creation)
    position = 0
    inJail = False  # Determines if player is currently in Jail or not
    # Get out of jail free cards held by player. One for chance and community chest draws.
    goojfChance = False
    goojfComm = False
    ownedProperties = []  # List of all owned property index keys

    def __init__(self, pName):
        self.name = pName
        self.wallet = 1500

    def setWallet(self, amount):
        self.wallet += amount

    def setPostion(self, roll):
        self.position += roll
        if self.position == 30:
            print('WENT TO JAIL \n\n\n')
            self.position = 40
        elif self.position > 39:
            self.position -= 40

    def setGivenPosition(self, location):
        self.position = location

    def setGoToJail(self):
        self.position = 40
        self.toggleInJail()

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

    def getPosition(self):
        return self.position

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

    def playerPayRequest(self, amount):
        if self.wallet > amount:
            self.wallet -= amount
        else:
            print('You need more money! Do you want to mortgage some of your properties?')

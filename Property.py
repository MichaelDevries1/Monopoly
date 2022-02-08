import math
from Monopoly import SimpleLocation


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
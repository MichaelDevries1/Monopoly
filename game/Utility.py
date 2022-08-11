import math

from game import Property


class Utility(Property):
    # Third level of objects for utility properties.
    rent1 = 4  # dice roll multiple received when a player lands on 1 owned utility
    rent2 = 10  # dice roll multiple received when a player lands on 2 owned utilities
    level = 0  # Current number of utilities owned by owner. 0=none, 1=1 utility, or 2=2 utilities

    def __init__(self, pType, pName, pCost):
        super().__init__(pType, pName, pCost)
        self.mortgageValue = self.cost / 2
        self.unmortgageCost = int(math.ceil(self.mortgageValue * 1.1))
        self.owner = ''
        self.isMortgaged = False

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def setOwner(self, new_owner):
        self.owner = new_owner

    def setLevel(self, new_level):
        self.level = new_level

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

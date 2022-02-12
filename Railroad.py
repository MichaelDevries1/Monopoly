from Monopoly import Property


class Railroad(Property):
    # Third level of objects for railroad properties.
    rent1 = 25  # rent received when a player lands on 1 owned railroad
    rent2 = 50  # rent received when a player lands on 2 owned railroads
    rent3 = 100  # rent received when a player lands on 3 owned railroads
    rent4 = 200  # rent received when a player lands on 4 owned railroads
    level = 0  # Current number of railroads owned by owner. 0=none, 1=1 railroad.. 4=all railroads.

    def __init__(self, pType, pName, pCost):
        super().__init__(pType, pName, pCost)
        self.owner = ''
        self.isMortgaged = False

    def toggleIsMortgaged(self):
        self.isMortgaged = not self.isMortgaged

    def setOwner(self, new_owner):
        self.owner = new_owner

    def setLevel(self, new_level):
        self.level = new_level

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

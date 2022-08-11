import math

from game import Property


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

from game import SimpleLocation


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

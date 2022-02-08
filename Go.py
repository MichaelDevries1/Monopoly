from Monopoly import SimpleLocation


class Go(SimpleLocation):
    # The Go location object. Requires the SimpleLocation object. Used to retrieve information for "Go"
    payment = 200

    def __init__(self, propType, cardName):
        super().__init__(propType, cardName)

    def getPayment(self):
        return self.payment

    def getInfo(self):
        return [self.type, self.name, self.payment]
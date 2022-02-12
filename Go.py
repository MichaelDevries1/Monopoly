from Monopoly import SimpleLocation


class Go(SimpleLocation):
    # The Go location object. Requires the SimpleLocation object. Used to retrieve information for "Go"
    payment = 200

    def __init__(self, prop_type, card_name):
        super().__init__(prop_type, card_name)

    def getPayment(self):
        return self.payment

    def getInfo(self):
        return [self.type, self.name, self.payment]

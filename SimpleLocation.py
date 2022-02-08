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
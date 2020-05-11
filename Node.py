


class Node(object):
    Latitude = None
    Longtitude = None
    NodeID = None
    arrival = None
    order = None
    date = None
    leaving = None
    cost = 0
    leftCapacity = 22000  ##after leaving a node
    isFinish = False
    Region = 1
    eklenmesirasi = -1
    waitingCost=-1
    def __init__(self,region, ID:int  ,Latitude:float,Longtitude:float):
        self.Latitude = Latitude
        self.Longtitude = Longtitude
        self.NodeID = ID
        self.arrival = None
        self.leaving =None
        self.order = None
        #For now our assumption is that same location there would be one pick or delivery
        self.isPickup = None
        self.isDelivered = None
        self.date=None
        self.isFinish=False
        self.region=region

    def getDate(self):
        return self.date

    def setDate(self, value):
        self.date = value

    @property
    def getArrival(self):
        return self.arrival

    def setLeaving(self, value):
        self.leaving = value

    def setArrival(self,value):
        self.arrival = value
    @property
    def getOrder(self):
        return self.order
    def setOrder(self,value):
        self.order = value

    @property
    def ispickup(self):
        return self.isPickup
    def setPickup(self,value,date):
        self.isPickup = value
        self.date=date


    @property
    def isdelivered(self):
        return self.isDelivered
    def setDelivered(self,value,date):
        self.isDelivered = value
        self.date = date
    def setLatitude(self,value):
        self.Latitude = value
        return self.Latitude

    @property
    def getLatitude(self):
        return self.Latitude

    @property
    def getLongtitude(self):
        return self.Longtitude
    @property
    def getNodeID(self):
        return self.NodeID

    def setLatitude(self,value):
        self.Latitude = value
        return self.Latitude
    def setLongtitude(self,value):
        self.Longtitude = value
        return self.Longtitude
    def setNodeID(self,value):
        self.NodeID = value
        return self.getNodeID()
    def str(self):
        return str(self.NodeID) + "  "  + str(self.Latitude) + "  " + str(self.Longtitude)

class Order(object):
    isAssigned = False
    weight = 0
    volume=0
    cluster=-1
    GidateTolerance=1
    D_dateTolerance=1


    max_waiting_tolerance=-1
    equipmentType=-1
    tripType=-1
    sub_mode=1

    transport_mode=""


    tourPickIndeks=-1
    tourDelIndeks=-1


    def __init__(self,L:int,origin,destination,	gi_date,
                 gi_date_tolerance,w_tolerance,didate,d_date_tolerance,
                 weight,volume,e_type,trip_type,transport,s_mode):
        self.isAssigned = False
        self.isDelivered =False
        self.orderID = L#good issue date
        self.gi_date = gi_date#good issue date
        self.d_date= didate  #deadline date
        self.p_date = None #pick up date
        self.r_date = None#reached date
        self.transport_mode=transport
        self.origin = origin #origin node index
        self.destination = destination#destinatiob node index

        self.assigned_t = None #assigned truck or cycle id
        self.volume = volume
        self.weight = weight

        self.GidateTolerance =gi_date_tolerance
        self.D_dateTolerance =d_date_tolerance

        self.max_waiting_tolerance=w_tolerance
        self.equipmentType=e_type
        self.tripType=trip_type
        self.sub_mode=s_mode


    def str(self):
        return "Order IDler:    " + str(self.orderID)
    @property
    def getOrderID(self):
        return self.orderID


    @property
    def getGidate(self):
        return self.gi_date

    @property
    def getD_date(self):
        return self.d_date
    def setGidate(self,value):
        self.gi_date = value
    def setOrigin(self,value):
        self.origin = value
    def setDestination(self,value):
        self.destination = value

    @property
    def getOrigin(self):
        return self.origin

    @property
    def getDestination(self):
        return self.destination

    def setisAssigned(self, value):
        self.isAssigned = value

    @property
    def getisAssigned(self):
        return self.isAssigned

    @property
    def getisdelivered(self):
        return self.isDelivered




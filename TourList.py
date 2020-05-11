

class TourList(object):

    cost=0
    tourID=-1
    tour=None

    def __init__(self,TourID,TourList):

        self.cost=self.CostOfTour(TourList)
        self.tourID=TourID
        self.tour=TourList





    def CostOfTour(self, list):

        if list is None:
            return 0
        cost = 0
        for node in list:
            cost += node.cost
        return cost


    def gettour(self):
        return self.tour
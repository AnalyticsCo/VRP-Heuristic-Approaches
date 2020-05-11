from itertools import islice

from datascience import *

path_data = '../../../../data/'
import matplotlib.pyplot as plots

plots.style.use('fivethirtyeight')
import math
import matplotlib
import datetime
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd
from math import sin, cos, sqrt, atan2
import sys
from random import randint
from Tour import *
import copy
from Node import *
from Order import *
from DataPrep import *
from TourList import *

import random
import tkinter
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import Equations
import TLModule


waitingcost = 20
cost_per_km = 0.8
Maxweight = 22000
TourCost = 0

daily_maxkm=720


class Metodlar():
    OrderNodeList = []
    AssignedOrder = []
    DeliveryQueue = []
    WholeTourLists = []
    ToursObjectList=[]


    #Calisilan siparis sayisi +1
    for i in range(0, 8):
        if (i == 0):
            AssignedOrder.append(1)
            continue
        AssignedOrder.append(0)

    Veri = None
    TourList = []

    # class methods(object):
    def __init__(self, value):
        self.Veri = value
        self.AssignedOrder

    def select_first_order(self):
        for order in self.Veri.OrderList:
            if len(order) == 0:  ## Patlama ihtimali olan durumlar icin control statementları yazilmali
                continue
            ###Ilk en yakın tarihli gordugu yuku alır # next generation algorithm we will implement listing next day potential then eliminate with circle
            if len(order) == 1 and self.AssignedOrder[order[0].getOrderID]!=1:
                return order[0]
            else:

                for ord in order:
                    if (self.AssignedOrder[ord.getOrderID]==1):
                        continue
                    else:
                        return ord




    def DogruDenklemiKatsayiArrayi(self, x1, y1, x2, y2):

        # Define the known points y=ax+b

        """
        x1=60*x1
        x2=60*x2
        y1=111*y1
        y2=111*y2
        """
        """
               Print the findings y = ax +b

               print
               'a =', coefficients[0]
               print
               'b =', coefficients[1]
               """

        slope = (y2 - y1) / ((x2 - x1) * 60 / 111)
        b = y1 - slope * x1
        katsayilar = []
        katsayilar.append(slope)
        katsayilar.append(b)
        return katsayilar
        # Calculate the coefficients. This line answers the initial question.

    # coefficients = np.polyfit(ilknokta, ikincinokta, 1)
    # print(coefficients)

    def costCalculation(self, indeks,TourList):

        Node = TourList[indeks]
        if indeks == 0:
            Node.cost = 0
            return 0

        travel_cost = (TourList[indeks].arrival - TourList[indeks - 1].leaving) * daily_maxkm * cost_per_km
        nodewaitingcost = (TourList[indeks].leaving - TourList[indeks].arrival) * waitingcost
        cost = travel_cost + nodewaitingcost

        return cost



    def AddingCost(self, Order,TourList):

        tourList = TourList
        queueList = self.DeliveryQueue
        LastNode = TourList[len(tourList) - 1]
        travelTime = self.Veri.distCalc(LastNode.NodeID, Order.getOrigin) / daily_maxkm
        leavingtime = LastNode.leaving

        if (leavingtime + travelTime < Order.getGidate):
            node_cikis_zamani = Order.getGidate
        else:
            node_cikis_zamani = leavingtime + travelTime
        hedefe_gelis_zamani = node_cikis_zamani

        if (len(queueList) >= 1):
            firstAddingCost = travelTime * daily_maxkm * cost_per_km + self.Veri.distCalc(queueList[0].NodeID,Order.getOrigin) * cost_per_km + (node_cikis_zamani - leavingtime - travelTime) * waitingcost
            LastAddingCost = self.Veri.distCalc(tourList[0].NodeID,Order.getDestination) * cost_per_km + self.Veri.distCalc(queueList[len(queueList) - 1].NodeID, Order.getDestination) * cost_per_km


        else:
            firstAddingCost = travelTime * daily_maxkm * cost_per_km + (node_cikis_zamani - leavingtime - travelTime) * waitingcost
            LastAddingCost = self.Veri.distCalc(tourList[0].NodeID, Order.getDestination) * cost_per_km+self.Veri.distCalc(Order.getDestination,Order.getOrigin)* cost_per_km

        return firstAddingCost + LastAddingCost

    def finding_potentialPie(self, NodeIndeks, Yaricap, Radius):

        # cur = TourList.Head
        # Node = cur.data
        NodeIndeks = int(NodeIndeks)
        OrderList = self.Veri.UnSortedOL

        Radius = math.radians(Radius / 2)
        center_Latitude = self.Veri.NodeList[NodeIndeks - 1].Latitude
        center_Longtitude = self.Veri.NodeList[NodeIndeks - 1].Longtitude

        first_point_Latitude = math.sin(Radius) * Yaricap / 111 + center_Latitude
        first_point_Longtitude = (math.cos(Radius)) * Yaricap / 60 + center_Longtitude

        second_point_Latitude = center_Latitude - math.sin(Radius) * Yaricap / 111
        second_point_Longtitude = math.cos(Radius) * Yaricap / 60 + center_Longtitude

        ilk_dogru_katsayilari = self.DogruDenklemiKatsayiArrayi(center_Longtitude, center_Latitude,
                                                                first_point_Longtitude, first_point_Latitude)
        ikinci_dogru_katsayilari = self.DogruDenklemiKatsayiArrayi(center_Longtitude, center_Latitude,
                                                                   second_point_Longtitude, second_point_Latitude)

        potentialOrder = []

        ##Gi date ve Delivery Date arasindaki siparislerin listeye eklenmesi
        for ord in OrderList:
            if (ord is None or self.AssignedOrder[ord.getOrderID] == 1):
                continue
            order_x = self.Veri.NodeList[ord.getOrigin - 1].Longtitude
            order_y = self.Veri.NodeList[ord.getOrigin - 1].Latitude
            if Equations.isInCircle(order_x,order_y,center_Longtitude,center_Latitude,Yaricap) \
                    and order_x * ilk_dogru_katsayilari[0] + ilk_dogru_katsayilari[1] <= order_y \
                    and order_x * ikinci_dogru_katsayilari[0] + ikinci_dogru_katsayilari[1] >= order_y:
                potentialOrder.append(ord)

            """
            order_x = 0
            order_y = 0
            x_array = []
            y_array = []

            for i in range(-daily_maxkm, 721):
                for j in range(-daily_maxkm, 721):
                    order_y = i/4
                    order_x = j/4
                    if ((order_y - center_Latitude) * 111) ** 2 + ((order_x - center_Longtitude) * 60) ** 2 <= (Yaricap) ** 2 \
                            and order_x* ilk_dogru_katsayilari[0] + ilk_dogru_katsayilari[1] >= order_y \
                            and order_x* ikinci_dogru_katsayilari[0] + ikinci_dogru_katsayilari[1] <= order_y:
                        x_array.append(order_x)
                        y_array.append(order_y)



            plt.scatter(x_array,y_array,1.5)
            plt.scatter(center_Longtitude,center_Latitude,color='red')
            plt.show()
        """
        return potentialOrder

    def SingleTripCost(self, Order):

        Origin = Order.getOrigin
        Destination = Order.getDestination
        distance = self.Veri.distCalc(Origin, Destination)
        travel_cost = distance * cost_per_km

        return travel_cost * 2


    def BaslangicaDonerkenPotansiyelBulma(self, TurunSonNod,BaslangicNode):

        Longtitude =TurunSonNode.getLongtitude
        Latitude =TurunSonNode.getLatitude
        leaving = TurunSonNode.leaving










    def finding_potentialCircle(self, NodeIndeks, r):

        # cur = TourList.Head
        # Node = cur.data
        NodeIndeks = int(NodeIndeks)
        OrderList = self.Veri.UnSortedOL
        Node_Latitude = self.Veri.NodeList[NodeIndeks - 1].Latitude
        Node_Longtitude = self.Veri.NodeList[NodeIndeks - 1].Longtitude

        potentialOrder = []
        ##Gi date ve Delivery Date arasindaki siparislerin listeye eklenmesi
        for ord in OrderList:
            if (ord is None or self.AssignedOrder[ord.getOrderID] == 1):
                continue
            order_x = self.Veri.NodeList[ord.getOrigin - 1].Latitude
            order_y = self.Veri.NodeList[ord.getOrigin - 1].Longtitude
            if Equations.isInCircle(order_x,order_y,Node_Longtitude,Node_Latitude,r):
                potentialOrder.append(ord)
        return potentialOrder

    def ElimanasyonIcinMaliyetHesabı(self,TourList):
        cost = 0

        for i in range(0, len(TourList)):
            cost += self.costCalculation(i)

        LastNode = TourList[len(TourList) - 1]
        costForDeliverQueue = 0
        for queue in self.DeliveryQueue:
            travel_cost = self.Veri.distCalc(queue.NodeID, LastNode.NodeID) * cost_per_km
            LastNode = queue
            costForDeliverQueue += travel_cost

        return costForDeliverQueue + cost + self.Veri.distCalc(LastNode.NodeID, TourList[0].NodeID) * cost_per_km


    def findingPotentialAddingLocation(self,Order,TourList):
        Gidate=Order.getGidate
        Gidate_tolerance =Order.GidateTolerance

        D_date=Order.getD_date
        D_date_tolerance =Order.D_dateTolerance
        potentialIndeks = [-1,-1,-1,-1]

        if TourList is None:
            potentialIndeks.append(0)
            return potentialIndeks





        for node in range(0,len(TourList)-1):
            if len(TourList)<2:
                break

            if self.Veri.UnSortedOL[TourList[node]].getDate < Gidate:
                    potentialIndeks[0]=node
            if self.Veri.UnSortedOL[TourList[node]].getDate < Gidate+Gidate_tolerance < self.Veri.UnSortedOL[TourList[node + 1]].getDate:
                    potentialIndeks[1]=node



        return potentialIndeks













    def potantialElimination(self, Node, PotentialList,TourList):
        LastNodeAtTour = TourList[len(TourList)-1]
        arrivaltime = Node.arrival
        leavingtime = Node.leaving
        silinecekPotansiyel = []
        count = 0

        for ord in PotentialList:

           # a =self.findingPotentialAddingLocation(ord ,TourList)
            count += 1
            travelTime = self.Veri.distCalc(Node.getNodeID, ord.getOrigin) / daily_maxkm
            node_cikis_zamani = 0
            single_trip_cost= self.SingleTripCost(ord)

            #If arrive before good issue date, wait
            if (leavingtime + travelTime < ord.getGidate):
                node_cikis_zamani = ord.getGidate
            else:
                node_cikis_zamani = leavingtime + travelTime
            hedefe_gelis_zamani = node_cikis_zamani

            #If Waiting time greater then maxiumun waiting or Max capacity not taking order
            if (node_cikis_zamani - leavingtime + travelTime > ord.max_waiting_tolerance) or \
                    (leavingtime + travelTime > ord.getGidate + ord.GidateTolerance) or LastNodeAtTour.leftCapacity-ord.weight <0:
                silinecekPotansiyel.append(ord)
                continue

            if (len(self.DeliveryQueue) > 0):
                destinationNode = copy.deepcopy(self.Veri.NodeList[ord.getDestination - 1])
                destinationNode.setDelivered(ord.getOrderID,ord.getD_date)
                self.DeliveryQueue.append(destinationNode)

                travelTime = self.Veri.distCalc(ord.getOrigin, self.DeliveryQueue[0].NodeID) / daily_maxkm
                addingCost = self.AddingCost(ord,TourList)
                differenceCost = addingCost - self.Veri.distCalc(LastNodeAtTour.NodeID,self.DeliveryQueue[0].NodeID)*cost_per_km - \
                                 self.Veri.distCalc(self.DeliveryQueue[len(self.DeliveryQueue) - 1].NodeID,
                                                    TourList[0].NodeID) * cost_per_km


                if (differenceCost>single_trip_cost):
                    silinecekPotansiyel.append(ord)
                    self.DeliveryQueue.remove(destinationNode)
                    continue


                isaret = 1
                for order_queue in self.DeliveryQueue:
                    if (hedefe_gelis_zamani + travelTime > self.Veri.UnSortedOL[order_queue.isdelivered].getD_date + self.Veri.UnSortedOL[order_queue.isdelivered].D_dateTolerance):
                        silinecekPotansiyel.append(ord)
                        break
                    hedefe_gelis_zamani = hedefe_gelis_zamani + travelTime
                    travelTime = self.Veri.distCalc(self.DeliveryQueue[isaret].NodeID, order_queue.NodeID) / daily_maxkm
                    isaret += 1
                    if (isaret > len(self.DeliveryQueue) - 1):
                        break
                self.DeliveryQueue.remove(destinationNode)

        for silinecekorder in silinecekPotansiyel:
            PotentialList.remove(silinecekorder)
        return PotentialList



    def findIndeks(self, Node,TourList):

        indeks = -1
        for node in TourList:
            indeks += 1
            if (node.getNodeID == Node.getNodeID):
                break
        return indeks



    #If returns -1 means this order not added this tours
    def detectingDeliverySequence(self,ord,TourList):
        LastNodeAtTour = TourList[len(TourList)-1]
        Leaving = LastNodeAtTour.leaving
        travel_time_origin_lastNode = self.Veri.distCalc(ord.getOrigin,LastNodeAtTour.NodeID)/daily_maxkm

    def detectingOriginSequence(self, ord, TourList):
        LastNodeAtTour = TourList[len(TourList) - 1]
        Leaving = LastNodeAtTour.leaving
        travel_time_origin_lastNode = self.Veri.distCalc(ord.getOrigin, LastNodeAtTour.NodeID) / daily_maxkm




    def TuraNodeekleyici(self, PotentialCircleList,TourList):

        secondOrder = PotentialCircleList[0]
        self.AssignedOrder[secondOrder.getOrderID] = 1
        SecondNodeOriginIndex = secondOrder.getOrigin - 1
        SecondNodeDestinationIndex = secondOrder.getDestination - 1
        DestinationNodeIndex = secondOrder.getDestination - 1

        SecondNode = copy.deepcopy(self.Veri.NodeList[SecondNodeOriginIndex])
        SecondNode.setPickup(secondOrder.getOrderID,secondOrder.getGidate)
        LastNodeAtTour = TourList[len(TourList) - 1]
        Son_Nodedan_Cikma_Zamani = LastNodeAtTour.leaving
        SecondNode.leftCapacity = LastNodeAtTour.leftCapacity - secondOrder.weight

        travelTime = self.Veri.distCalc(LastNodeAtTour.NodeID, SecondNode.NodeID) / daily_maxkm

        Second_Noda_Gelme_Zamani = Son_Nodedan_Cikma_Zamani + travelTime
        Second_Nodedan_Cikma_Zamani = 0
        if Second_Noda_Gelme_Zamani < secondOrder.getGidate:
            Second_Nodedan_Cikma_Zamani = secondOrder.getGidate
        else:
            Second_Nodedan_Cikma_Zamani = Son_Nodedan_Cikma_Zamani + travelTime

        SecondNode.setArrival(Second_Noda_Gelme_Zamani)
        SecondNode.setLeaving(Second_Nodedan_Cikma_Zamani)
        TourList.append(SecondNode)
        SecondNode.cost = self.costCalculation(len(TourList) - 1,TourList)

        SecondDestinationNode = copy.deepcopy(self.Veri.NodeList[SecondNodeDestinationIndex])
        SecondDestinationNode.setDelivered(secondOrder.getOrderID,secondOrder.getD_date)
        self.DeliveryQueue.append(SecondDestinationNode)

    def baslangicaDonusNodeEkleyici(self, TourList):

        LastNodeAtTour=TourList[len(TourList)-1]
        indeks = int(TourList[0].NodeID)
        endingNode = copy.deepcopy(self.Veri.NodeList[indeks - 1])

        LeavingTime = LastNodeAtTour.leaving
        travelTime = self.Veri.distCalc(LastNodeAtTour.NodeID, endingNode.NodeID) / daily_maxkm
        endingNode.setLeaving(LeavingTime + travelTime)
        endingNode.leftCapacity = Maxweight
        endingNode.setArrival(LeavingTime + travelTime)
        TourList.append(endingNode)
        endingNode.cost = travelTime * daily_maxkm * cost_per_km
        endingNode.isFinish = True

    def TuraDestinationEkleyici(self, LastNodeAtTour,TourList):
        if (len(self.DeliveryQueue) == 0):
            return

        QueueList = self.DeliveryQueue
        DestinationNode = QueueList[0]
        DeliveredWeight = self.Veri.UnSortedOL[DestinationNode.isDelivered].weight
        LeavingTime = LastNodeAtTour.leaving
        travelTime = self.Veri.distCalc(LastNodeAtTour.NodeID, DestinationNode.NodeID) / daily_maxkm

        DestinationNode.setLeaving(LeavingTime + travelTime)
        DestinationNode.leftCapacity = LastNodeAtTour.leftCapacity + DeliveredWeight
        DestinationNode.setArrival(LeavingTime + travelTime)
        TourList.append(DestinationNode)
        DestinationNode.cost = self.costCalculation(len(TourList) - 1,TourList)

        QueueList.remove(DestinationNode)

    def addingFirstNode(self,TourList):



        FirstOrder = self.select_first_order()
        self.AssignedOrder[FirstOrder.getOrderID] = 1
        OriginNodeIndex = FirstOrder.getOrigin - 1
        DestinationNodeIndex = FirstOrder.getDestination - 1

        # Initializing the origin node by using order attributes
        OriginNode = copy.deepcopy(self.Veri.NodeList[OriginNodeIndex])
        OriginNode.setPickup(FirstOrder.getOrderID,FirstOrder.getGidate)
        OriginNode.setArrival(FirstOrder.getGidate)
        OriginNode.setLeaving(FirstOrder.getGidate)
        OriginNode.leftCapacity = OriginNode.leftCapacity - FirstOrder.weight

        TourList.append(OriginNode)
        OriginNode.cost = self.costCalculation(0,TourList)
        DestinationNode = copy.deepcopy(self.Veri.NodeList[DestinationNodeIndex])
        DestinationNode.setDelivered(FirstOrder.getOrderID,FirstOrder.getD_date)
        self.DeliveryQueue.append(DestinationNode)


    def CompleteTourList(self,TourList):

        if (len(TourList) == 0):
            self.addingFirstNode(TourList)

        LastNodeAtTour = TourList[len(TourList) - 1]
        PotentialCircleList = self.finding_potentialCircle(LastNodeAtTour.NodeID, 10000)
        PotentialCircleList = self.potantialElimination(LastNodeAtTour, PotentialCircleList, TourList)
        if (len(PotentialCircleList) == 0 and len(self.DeliveryQueue) == 0):
            self.baslangicaDonusNodeEkleyici(TourList)
            """


            Sonradan yazilacak 8 mart 

            for i in self.AssignedOrder:
                if i ==0:
                self.DeliveryQueue = []
            """

            return
        if (len(PotentialCircleList) == 0 and len(self.DeliveryQueue) > 0):
            self.TuraDestinationEkleyici(LastNodeAtTour, TourList)
        elif len(PotentialCircleList) >= 1:
            self.TuraNodeekleyici(PotentialCircleList, TourList)
        return self.CompleteTourList(TourList)

    def runtours(self):
        now = datetime.datetime.now()
        counter=1
        while True:

            totalAssigned = 0
            for i in self.AssignedOrder:
                totalAssigned += i


            if totalAssigned >= len(self.AssignedOrder):
                break
            tourList = []
            self.CompleteTourList(tourList)
            self.WholeTourLists.append(tourList)
            print("   Gecen Zaman                            " + str(datetime.datetime.now() - now)+"     Ekledigi Tur "+str(counter)+"\tTur uzunlugu"+str(len(self.WholeTourLists[counter-1])))
            counter+=1

        for i in range(len(self.WholeTourLists)):
            self.ToursObjectList.append(TourList(i+1,self.WholeTourLists[i]))

        TLModule.writeExcelResult(Veri, self.ToursObjectList)


now = datetime.datetime.now()
Veri = DataPrep('sezgisel.xlsx', 'Node', 'Order','Equipment','DistanceMatrix','TimeMatrix')  # Veri cekilme islemi ve data prep class ın objesi

Method_Object = Metodlar(Veri)
"""
TourList=[]
Method_Object.CompleteTourList(TourList)
Method_Object.WholeTourLists.append(TourList)
newTourList=[]
Method_Object.CompleteTourList(newTourList)
Method_Object.WholeTourLists.append(newTourList)
newTourList=[]
Method_Object.CompleteTourList(newTourList)
Method_Object.WholeTourLists.append(newTourList)

newTourList=[]
Method_Object.CompleteTourList(newTourList)
Method_Object.WholeTourLists.append(newTourList)
"""
Method_Object.runtours()
ObjectiveCost=0
for list in Method_Object.WholeTourLists:
    for cur in list:
        ObjectiveCost+=cur.cost
        if (cur.ispickup is not None and cur.isdelivered is None):
            print("Node Id :" + str(int(cur.getNodeID)) + "\tAlmak icin gelinen siparis =  " + str(
                int(cur.ispickup)) + "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(cur.cost))
        elif (cur.ispickup is None and cur.isdelivered is not None):
            print("Node Id :" + str(int(cur.getNodeID)) + "\tTeslim icin gelinen siparis =  " + str(
                int(cur.isdelivered)) + "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(cur.cost))
        else:
            print("Node Id :" + str(int(cur.getNodeID)) + "\tNode'a gelis = " + str(
                cur.arrival) + "\tNode'a ayrilis = " + str(cur.leaving) + "\t Kalan Yuk Kapasites = " + str(
                cur.leftCapacity) + "\t Node Costu = " + str(cur.cost))

    print("                                    ")
    print("                                    ")
    print("                                    ")

print("   OBJECTIVE ESITTIR                                 "+ str(ObjectiveCost))





















































# BirinciTur[] Sonradan yazilacak


""""
PotentialCircleList = Method_Object.finding_potentialCircle(FirstOrder.getOrigin, 10000)
PotentialPieList = Method_Object.finding_potentialPie(FirstOrder.getOrigin, daily_maxkm, 120)
PotentialCircleList = Method_Object.potantialElimination(Method_Object.TourList[0], PotentialCircleList)
"""


"""
Method_Object.TuraNodeekleyici(PotentialCircleList)

LastNodeAtTour = Method_Object.TourList[len(Method_Object.TourList)-1]
PotentialCircleList = Method_Object.finding_potentialCircle(LastNodeAtTour.NodeID,1000)
PotentialCircleList = Method_Object.potantialElimination(LastNodeAtTour,PotentialCircleList)
if(len(PotentialCircleList)==0):
    Method_Object.TuraDestinationEkleyici(LastNodeAtTour)
else:
    Method_Object.TuraNodeekleyici(PotentialCircleList)

LastNodeAtTour = Method_Object.TourList[len(Method_Object.TourList)-1]
PotentialCircleList = Method_Object.finding_potentialCircle(LastNodeAtTour.NodeID,1000)
PotentialCircleList = Method_Object.potantialElimination(LastNodeAtTour,PotentialCircleList)

if(len(PotentialCircleList)==0):
    Method_Object.TuraDestinationEkleyici(LastNodeAtTour)
else:
    Method_Object.TuraNodeekleyici(PotentialCircleList)


LastNodeAtTour = Method_Object.TourList[len(Method_Object.TourList)-1]
PotentialCircleList = Method_Object.finding_potentialCircle(LastNodeAtTour.NodeID,1000)
PotentialCircleList = Method_Object.potantialElimination(LastNodeAtTour,PotentialCircleList)

if(len(PotentialCircleList)==0):
    Method_Object.TuraDestinationEkleyici(LastNodeAtTour)
else:
    Method_Object.TuraNodeekleyici(PotentialCircleList)

LastNodeAtTour = Method_Object.TourList[len(Method_Object.TourList)-1]
PotentialCircleList = Method_Object.finding_potentialCircle(LastNodeAtTour.NodeID,1000)
PotentialCircleList = Method_Object.potantialElimination(LastNodeAtTour,PotentialCircleList)

if(len(PotentialCircleList)==0):
    Method_Object.TuraDestinationEkleyici(LastNodeAtTour)
else:
    Method_Object.TuraNodeekleyici(PotentialCircleList)


print(str(len(PotentialCircleList))+"....................")

"""


""""
count = 1
for node1 in Method_Object.Veri.NodeList:

    Nodei = []
    for node2 in Method_Object.Veri.NodeList:
        Nodei.append(Method_Object.Veri.distCalcScietificly(node1.NodeID,node2.NodeID))
        print(Method_Object.Veri.distCalcScietificly(node1.NodeID,node2.NodeID),end = "    ")
    print("")
    table.with_column(str(count)+".Node",Nodei)
    count+=1

print(table)
"""

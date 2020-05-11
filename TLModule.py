path_data = '../../../../data/'
import matplotlib.pyplot as plots

plots.style.use('fivethirtyeight')
import math
import matplotlib
import datetime
matplotlib.use('TkAgg')
from random import randint
import Equations
import copy
from Node import *
from Order import *
import DataPrep
import xlsxwriter
import itertools


def writeExcelResult(Veri,WholeTourList):

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    labels=['TurID','Sehir ID','Siparis ID','Alim/Teslimat','Gelis Zamanı','Ayrilis Zamani','Bekleme Suresi','Maks Date','Sehir Maliyeti']
    # Start from the first cell. Rows and columns are zero indexed.
    row1 = 0
    col1 = 0

    # Iterate over the data and write it out row by row.
    for i in range(0, len(labels)):
        worksheet.write(row1, col1, labels[i],bold)
        col1+= 1

    row1 = 1
    col1 = 0


    ObjectiveCost = 0
    for List in WholeTourList:

        col2=0


        for cur in List.tour:
            col1=0
            worksheet.write(row1, col1, List.tourID)
            col1+=1
            ObjectiveCost += cur.cost
            if (cur.ispickup is not None and cur.isdelivered is None):
                worksheet.write(row1, col1, cur.getNodeID)
                worksheet.write(row1, col1+1, cur.ispickup)
                worksheet.write(row1, col1+2, 'Alim')
                worksheet.write(row1, col1+3, cur.arrival)
                worksheet.write(row1, col1+4, cur.leaving)
                worksheet.write(row1, col1+5, cur.leaving-cur.arrival)
                worksheet.write(row1, col1+6, cur.date+Veri.UnSortedOL[cur.ispickup].GidateTolerance)
                worksheet.write(row1, col1+7, cur.cost)


            elif (cur.ispickup is None and cur.isdelivered is not None):
                worksheet.write(row1, col1, cur.getNodeID)
                worksheet.write(row1, col1+1, cur.isdelivered)
                worksheet.write(row1, col1+2, 'Teslim')
                worksheet.write(row1, col1+3, cur.arrival)
                worksheet.write(row1, col1+4, cur.leaving)
                worksheet.write(row1, col1+5, cur.leaving-cur.arrival)
                worksheet.write(row1, col1+6, cur.date+Veri.UnSortedOL[cur.isdelivered].D_dateTolerance)
                worksheet.write(row1, col1+7, cur.cost)


            else:

                worksheet.write(row1, col1, cur.getNodeID)
                worksheet.write(row1, col1+1, cur.isdelivered)
                worksheet.write(row1, col1+2, 'Tur Sonu')
                worksheet.write(row1, col1+3, cur.arrival)
                worksheet.write(row1, col1+4, '-')
                worksheet.write(row1, col1+5, '-')
                worksheet.write(row1, col1+6, '-')
                worksheet.write(row1, col1+7, cur.cost)

            row1+=1





    workbook.close()
def PrintTourList(List):
    ObjectiveCost = 0

    for cur in List:
        ObjectiveCost += cur.cost
        if (cur.ispickup is not None and cur.isdelivered is None):
            print("Node Id :" + str(int(cur.getNodeID)) + "\tAlmak icin gelinen siparis =  " + str(
                int(cur.ispickup)) + "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(
                cur.cost) + "\t Node date = " + str(cur.date))
        elif (cur.ispickup is None and cur.isdelivered is not None):
            print("Node Id :" + str(int(cur.getNodeID)) + "\tTeslim icin gelinen siparis =  " + str(
                int(cur.isdelivered)) + "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(
                cur.cost) + "\t Node date = " + str(cur.date))
        else:
            print("Node Id :" + str(int(cur.getNodeID)) + "\tNode'a gelis = " + str(
                cur.arrival) + "\tNode'a ayrilis = " + str(cur.leaving) + "\t Kalan Yuk Kapasites = " + str(
                cur.leftCapacity) + "\t Node Costu = " + str(cur.cost))



    print("   OBJECTIVE ESITTIR                                 " + str(ObjectiveCost))



def WholeTourListCost(WholeList):
    ObjectiveCost = 0
    for List in WholeList:
        for cur in List:
            ObjectiveCost += cur.cost
    return ObjectiveCost

def PrintWholeTourList(WholeList):
    ObjectiveCost = 0
    for List in WholeList:
        for cur in List:
            ObjectiveCost += cur.cost
            if (cur.ispickup is not None and cur.isdelivered is None):
                print("Node Id :" + str(int(cur.getNodeID)) + "\tAlmak icin gelinen siparis =  " + str(
                    + int(cur.ispickup)) + "\tEklenme Sirasi =  " + str(cur.eklenmesirasi)+ "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                    cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(
                    cur.cost) + "\t Node date = " + str(cur.date))
            elif (cur.ispickup is None and cur.isdelivered is not None):
                print("Node Id :" + str(int(cur.getNodeID)) + "\tTeslim icin gelinen siparis =  " + str(
                    int(cur.isdelivered)) +"\tEklenme Sirasi =  " + str(cur.eklenmesirasi)+ "\tNode'a gelis = " + str(cur.arrival) + "\tNode'a ayrilis = " + str(
                    cur.leaving) + "\t Kalan Yuk Kapasites = " + str(cur.leftCapacity) + "\t Node Costu = " + str(
                    cur.cost) + "\t Node date = " + str(cur.date))
            else:
                print("Node Id :" + str(int(cur.getNodeID)) +"\tEklenme Sirasi =  " + str(cur.eklenmesirasi)+ "\tNode'a gelis = "  +str(
                    cur.arrival) + "\tNode'a ayrilis = " + str(cur.leaving) + "\t Kalan Yuk Kapasites = " + str(
                    cur.leftCapacity) + "\t Node Costu = " + str(cur.cost))
        print(" ")
        print(" ")
        print(" ")
    print("   OBJECTIVE ESITTIR                                 " + str(ObjectiveCost))

def swapNodes(Node1,Node2,TourList):




    index1 = TourList.index(Node1)
    index2 = TourList.index(Node2)
    if(Node1.isPickup is not None and Node2.isDelivered is not None and Node2.isDelivered == Node1.isPickup or index1==index2):
        return -1


    TourList[index1], TourList[index2] = TourList[index2], TourList[index1]

    return index1


def TourElimination(TourList):

    if TourList[0].isDelivered is not None:
        return False

    org_indeks=0
    dest_indeks=0
    for nodeO in TourList:

        if nodeO.isPickup is not None:
            for nodeD in TourList:
                if nodeD.isDelivered is not None and nodeO.isPickup == nodeD.isDelivered and org_indeks>dest_indeks:
                    return False
                dest_indeks +=1
            dest_indeks = 0
        org_indeks += 1
    return True


def isDelayAtQueue(leaving,NodeID,Veri,queuelist,daily_maxkm):


        hedefe_gelis_zamani = leaving
        travelTime = Veri.distCalc(NodeID, queuelist[0].NodeID) / daily_maxkm
        isaret = 1
        for order_queue in queuelist:
            if (hedefe_gelis_zamani + travelTime > Veri.UnSortedOL[order_queue.isdelivered].getD_date+Veri.UnSortedOL[order_queue.isdelivered].D_dateTolerance):
                return True

            isaret += 1
            if (isaret > len(queuelist) - 1):
                return False
            hedefe_gelis_zamani = hedefe_gelis_zamani + travelTime
            travelTime = Veri.distCalc(queuelist[isaret].NodeID, order_queue.NodeID) / daily_maxkm

        return False


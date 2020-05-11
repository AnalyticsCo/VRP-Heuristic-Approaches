from datascience import *
path_data = '../../../../data/'
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')
import math
import numpy as np
from scipy import stats
import pandas as pd
from math import sin, cos, sqrt, atan2
import sys

import  copy
from Node import *
from Order import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

NodeList = []
OrderList = []
UnSortedOL = []
Equipment_Table=Table()

class DataPrep(object):
    Equipment_Table=Table()
    distanceMatrix=[[]]
    timeMatrix=[[]]
    def __init__(self, D_path, nodesheet, ordersheet,equipmentsheet,DistanceMatrix,TimeMatrix):
        self.NodeList = self.Node_initialize(self.read_data(D_path, nodesheet))
        self.OrderList = self.Sorted_Order_initialize(self.read_data(D_path, ordersheet))
        self.UnSortedOL =self.UnSorted_Order_initialize(self.read_data(D_path, ordersheet))
        self.eqipment_initialize(self.read_data(D_path, equipmentsheet))
        self.distanceMatrixInitialize(self.read_data(D_path, DistanceMatrix))
        self.timeMatrixInitialize(self.read_data(D_path, TimeMatrix))



        #self.KmeanCluster()
    def read_data(self, D_path, sheet):
        a =pd.read_excel(D_path, sheet)

        return a

    def eqipment_initialize(self,Data):

        self.Equipment_Table=Table.from_df(Data)


        return

    def distanceMatrixInitialize(self,Data):

        #df = pd.read_excel('sezgisel_11lik.xlsx','DistanceMatrix')

        A_Data = Data.to_numpy()
        self.distanceMatrix=A_Data[1:,2:]

    def timeMatrixInitialize(self,Data):

        #df = pd.read_excel('sezgisel_11lik.xlsx','DistanceMatrix')

        A_Data = Data.to_numpy()
        self.timeMatrix=A_Data[1:,2:]






    def  KmeanCluster(self):
        origin_x = []
        origin_y =[]
        dest_x=[]
        dest_y=[]
        gi_date=[]
        d_date=[]
        cluster=[]
        for ord in self.UnSortedOL:
            if(ord is None):
                continue
            origin_x.append(self.NodeList[ord.getOrigin-1].getLongtitude)
            origin_y.append(self.NodeList[ord.getOrigin-1].getLatitude)
            dest_x.append(self.NodeList[ord.getDestination-1].getLongtitude)
            dest_y.append(self.NodeList[ord.getDestination-1].getLatitude)
            gi_date.append(ord.getGidate)
            d_date.append((ord.getD_date))
        Data = {
            'o_x': origin_x,
            'o_y': origin_y,
            'd_x':dest_x,
            'd_y':dest_x,
            'gdate': gi_date,
            'ddate':d_date

        }

        df = DataFrame(Data, columns=['o_x', 'o_y','d_x','d_y','gdate','ddate'])

        df_std = StandardScaler().fit_transform(df)
        kmeans = KMeans(n_clusters=10).fit(df)
        centroids = kmeans.cluster_centers_

        for ord in self.UnSortedOL:
            if(ord is None):
                continue

            ord.cluster =kmeans.predict(make_array(origin_x[ord.getOrderID-1],origin_y[ord.getOrderID-1],
                                                   dest_x[ord.getOrderID-1],dest_y[ord.getOrderID-1],
                                                   gi_date[ord.getOrderID-1],d_date[ord.getOrderID-1]).reshape(1, -1))
            cluster.append(ord.cluster)

        plt.scatter(origin_x, origin_y,  s=10, cmap='viridis')
        plt.scatter(dest_x, dest_y, s=10, cmap='viridis')
        centers = kmeans.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.5)
        plt.show()




        return




    def Node_initialize(self,Data):
        List = []
        A_Data = Data.to_numpy()
        for row in np.arange(0,Data.shape[0]):
            dummylist =[]
            for column in np.arange(0, Data.shape[1]):
                dummylist.append(A_Data[row,column])
            Dummy_Node= Node(dummylist[0], dummylist[1], dummylist[2], dummylist[3])
            List.append(Dummy_Node)
            dummylist.clear()
        return List

    def distCalcScietificly(self,nodeOne,nodeTwo):

        R = 6371

        nodeOne = int(nodeOne) - 1
        nodeTwo = int(nodeTwo) - 1
        lat1 = math.radians(self.NodeList[nodeOne].getLatitude)
        lon1 = math.radians(self.NodeList[nodeOne].getLongtitude)
        lat2 = math.radians(self.NodeList[nodeTwo].getLatitude)
        lon2 = math.radians(self.NodeList[nodeTwo].getLongtitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def UnSorted_Order_initialize(self, Data):
        List = []
        List.append(None)
        A_Data = Data.to_numpy()
        for row in np.arange(0, Data.shape[0]):
            dummylist = []
            for column in np.arange(0, Data.shape[1]):
                dummylist.append(A_Data[row, column])
            Dummy_Order = Order(dummylist[0], dummylist[1], dummylist[2], dummylist[3], dummylist[4], dummylist[5],
                                dummylist[6],dummylist[7],dummylist[8],dummylist[9],
                                dummylist[10],dummylist[11],dummylist[12],dummylist[13])

            List.append(Dummy_Order)
            dummylist.clear()
        return List

    def Sorted_Order_initialize(self, Data):
        List = []
        for i in range (0,500):
            dummylist =[]
            List.append(dummylist)
        A_Data = Data.to_numpy()
        for row in np.arange(0,Data.shape[0]):
            dummylist = []
            for column in np.arange(0, Data.shape[1]):
                dummylist.append(A_Data[row,column])
            Dummy_Order= Order(dummylist[0], dummylist[1], dummylist[2], dummylist[3], dummylist[4], dummylist[5],
                               dummylist[6],dummylist[7],dummylist[8],dummylist[9],dummylist[10],dummylist[11],dummylist[12],dummylist[13])

            List[Dummy_Order.getGidate].append(Dummy_Order)
            dummylist.clear()
        return List


    def distCalc(self,nodeOne,nodeTwo):

        nodeOne =int(nodeOne)-1
        nodeTwo =int(nodeTwo)-1
        lat1 = self.NodeList[nodeOne].getLatitude
        lon1 = self.NodeList[nodeOne].getLongtitude
        lat2 = self.NodeList[nodeTwo].getLatitude
        lon2 = self.NodeList[nodeTwo].getLongtitude

        dlon = abs(lon2 - lon1) * 60
        dlat = abs(lat2 - lat1) * 111

        distance = sqrt(dlon ** 2 + dlat ** 2)

        return distance






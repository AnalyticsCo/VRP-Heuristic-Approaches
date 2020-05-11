

def isInCircle(order_x,order_y,center_Longtitude,center_Latitude,Yaricap):

    if((order_x - center_Longtitude) * 60) ** 2 + ((order_y - center_Latitude) * 111) ** 2 <= Yaricap ** 2:
        return True
    else:
        return False




def DogruDenklemiKatsayiArrayi( x1, y1, x2, y2):

     # Define the known points y=ax+b

    """
        x1=60*x1
        x2=60*x2
        y1=111*y1
        y2=111*y2

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


def IkiNoktasiBilinendogruDenklemi(X,x1, y1, x2, y2):

    katsayilar =  DogruDenklemiKatsayiArrayi(x1, y1, x2, y2)
    return X*katsayilar[0]+katsayilar[1]


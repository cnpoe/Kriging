from geostatsmodels import utilities, variograms, model, kriging, geoplot
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

#Aqui se obtienen los datos
z = utilities.readGeoEAS('C:\Users\lmorales\Desktop\geostatsmodels\data\ZoneA.dat')
P = z[:,[0,1,3]]

def getPoints(nrow, ncol, large, width):
    res = []
    dx = large / (ncol + 1)
    dy = width / (nrow + 1)

    yv = dy
    for i in range(0, nrow + 1):
        xv = dx
        for j in range(0, ncol + 1):
            #print "(i,j): " + str(xv) + " " + str(yv)
            if xv == yv:
                xv = xv + 1
            res.append({"x": xv, "y": yv})
            xv = xv + dx
        yv = yv + dy
    return res

def calcularVecindad(punto, P):
    nnearest = 0
    max_distance = 2500
    for point in P:
        distance = ( (punto[0] - point[0]) ** 2 + (punto[1] - point[1]) ** 2) **0.5 
        if distance < max_distance:
            nnearest = nnearest + 1
            #print "distancia = " + str(distance) + " x = " + str(point[0]) + " y = " + str(point[1]) + " value = " + str(point[2])
    return nnearest

def calculaKriging(punto, P, N, d):
    #print N
    #print punto
    x = punto[0]
    y = punto[1]
    #tolerance = 250
    #lags = np.arange( tolerance, 10000, tolerance*2 )
    sill = np.var( P[:,2] )
    #geoplot.semivariogram( P, lags, tolerance )
    svm = model.semivariance( model.spherical, ( 4000, sill ) )
    #geoplot.semivariogram( P, lags, tolerance, model=svm )
    covfct = model.covariance( model.spherical, ( 4000, sill ) )
    #kriging.simple( P, covfct, pt, N=6 )

    kriging.ordinary( P, covfct, punto, N )

    est, kstd = kriging.krige( P, covfct, [[x,y],[x+d,y],[x,y+d],[x+d,y+d]], 'ordinary', N )
    #print est
    #print kstd
    return est

nrow = 10
ncol = 10

minx = 1000000
miny = 1000000
maxx = 0
maxy = 0

for point in P:
    minx = point[0] if minx > point[0] else minx
    miny = point[1] if miny > point[1] else miny
    maxx = point[0] if maxx < point[0] else maxx
    maxy = point[1] if maxy < point[1] else maxy
#print "minx = " + str(minx) + " miny = " + str(miny) + " maxx = " + str(maxx) + " maxy = " + str(maxy)

points = getPoints(nrow, ncol, maxx + miny, maxy + miny)

#print "POINTS"
#for point in points:
#    print point




counter = 0
for point in points:
    #counter = counter + 1
    #print "Punto numero: " + str(counter)
    #print point
    N = calcularVecindad([point["x"], point["y"]], P)
    if N <= 2: 
        N = 3
    #point["valor"] = calculaKriging([point.x, point.y], P, N, d)
    if counter == nrow + 1:
        counter = 0
        print ""
    val = calculaKriging([point["x"], point["y"]], P, N, 100)[0][0]
    val = val if val > 0 else 0.0
    print val,
    counter = counter + 1



#print points
#python 3.8.1
from matplotlib import pyplot
from numpy import *
from multiprocessing import Pool
from sympy import *
#ALL UNITS ARE INCHES AND SECONDS AND DEGREES
#shooter height
shooterY = 13.5
#legal height and distance
legalY = 5.0*12 + shooterY
legalX = 11.0*12
#shooter max velocity
shooterMaxV = 345.575
#shooting location
shootDistMax = 11
shootDistMin = 6
#measurements of goal
goalMax = 38.625
goalMin = 33.125
#angles to test
angleMax = 90
angleMin = 0
#increase this value for more precise calculations but longer run time
p = 1.0

def getAngles(precision):
    testAngles = []
    for angle in arange(angleMin,angleMax+0.1,5/p):
        testAngles.append(angle)

    return testAngles

def getDistances(precision):
    testDistances = []
    for distance in arange(shootDistMin, shootDistMax+0.1, 1/p):
        testDistances.append(distance)

    return testDistances

def getVelocity(angle, distance):
    #two possible velocities from height
    v = Symbol('v')
    vVal1 = solveset(Eq((goalMax-shooterY),(math.sin(angle*math.pi/360.0)*v*(distance/(math.cos(angle*math.pi/360.0))))-(0.5*9.8*(distance/(math.cos(angle*math.pi/360.0)))**2)), v)
    vVal2 = solveset(Eq((goalMin-shooterY),(math.sin(angle*math.pi/360.0)*v*(distance/(math.cos(angle*math.pi/360.0))))-(0.5*9.8*(distance/(math.cos(angle*math.pi/360.0)))**2)), v)

    return vVal1, vVal2

def checkValidV(v, angle):
    if v <= shooterMaxV:
        timeMaxHeight = v*sin(angle*math.pi/360.0)/9.8
        maxHeight = (math.sin(angle*math.pi/360.0)*v*timeMaxHeight)-(0.5*9.8*timeMaxHeight**2)
        if maxHeight <= legalY:
            maxDistance = timeMaxHeight*(math.cos(angle*math.pi/360.0))*v
            if maxDistance <= legalX:
                return True

    return False

def getPercentHit(vars):
    angle = vars[0]
    distances = vars[1]

    totalIn = 0.0
    for i in range(len(distances)):
        v1,v2 = getVelocity(angle, distances[i])
        if len(v1) != 0:
            IN1 = checkValidV(v1[0], angle)
        if len(v1) != 0:
            IN2 = checkValidV(v2[0], angle)
        if IN1 or IN2:
            totalIn += 1

    percentIn = totalIn/i*100
    return percentIn

def displayResults(testAngles, percentInResults):
    fig = pyplot.figure("Percent In vs Angle")
    fig.tight_layout()
    plt = fig.add_subplot(111)
    plt.set_facecolor('b')
    plt.scatter(testAngles, percentInResults, c='yellow', marker='s', alpha=0.5)
    pyplot.subplots_adjust(hspace = 0.4)
    pyplot.show()

    return

def main():
    testAngles = getAngles(p)
    testDistances = getDistances(p)

    vars = []
    for x in range(len(testAngles)):
        vars.append([testAngles[x],testDistances])

    print(vars)
    #CHANGE PROCESSES TO HOWEVER MANY CORES U HAVE
    with Pool(processes=4, maxtasksperchild = 1) as pool:
            percentInResults = pool.map(getPercentHit, vars)
            pool.close()
            pool.join()

    displayResults(testAngles, percentInResults)

if __name__ == '__main__':
	main()

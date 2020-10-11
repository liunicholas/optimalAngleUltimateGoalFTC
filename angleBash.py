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
legalX = 16.0*12
#shooter max velocity
shooterMaxV = 345.575
#shooting location
shootDistMax = 11*12
shootDistMin = 6*12
#measurements of goal
goalMax = 38.625
goalMin = 33.125
#angles to test
angleMax = 80
angleMin = 0
#increase this value for more precise calculations but longer run time
p = 3.0

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
    # print(distance)
    #two possible velocities from height
    v = Symbol('v')
    # t = (distance/(cos(radians(angle))*v))
    vVal1 = solveset(Eq((goalMax-shooterY),(sin(radians(angle))*v*(distance/(cos(radians(angle))*v)))-(0.5*32.1522*((distance/(cos(radians(angle))*v))**2))), v)
    vVal2 = solveset(Eq((goalMin-shooterY),(sin(radians(angle))*v*(distance/(cos(radians(angle))*v)))-(0.5*32.1522*((distance/(cos(radians(angle))*v))**2))), v)

    # print(vVal1,vVal2)
    v1, v2 = list(vVal1), list(vVal2)
    print(v1,v2)
    # v1 = [x for x in v1 if isinstance(x, float)]
    # v2 = [x for x in v2 if isinstance(x, float)]
    # print(v1,v2)
    return v1, v2

def checkValidV(v, angle, distance):
    print(f"valid velocity: {v}")
    print(f"angle: {angle}")
    print(f"distance: {distance}")
    if v <= shooterMaxV:
        timeMaxHeight = v*sin(radians(angle))/32.1522
        # print(timeMaxHeight)
        maxHeight = (sin(radians(angle))*v*timeMaxHeight)-(0.5*32.1522*timeMaxHeight**2)
        print("max height ", maxHeight)
        if maxHeight <= legalY:
            # print("valid height")
            t = Symbol('t')
            time = solveset(Eq((-1*shooterY),(sin(radians(angle))*v*t)-(0.5*32.1522*(t**2))), t)
            time = list(time)
            maxDistance = abs(time[1])*(cos(radians(angle)))*v
            print("max distance ", maxDistance)
            if maxDistance <= legalX:
                print("valid distance")
                return True

    return False

def getPercentHit(vars):
    # print("trying")
    angle = vars[0]
    distances = vars[1]

    totalIn = 0.0
    for i in range(len(distances)):
        IN1, IN2 = False, False
        v1,v2 = getVelocity(angle, distances[i])
        IN1 = checkValidV(v1[1], angle, distances[i])
        IN2 = checkValidV(v2[1], angle, distances[i])
        # if len(v1) != 0:
        #     for item in v1:
        #         if item >= 0:
        #             v = item
        #             IN1 = checkValidV(v, angle, distance)
        #         # try:
        #         #     if item >= 0:
        #         #         v = item
        #         #         IN1 = checkValidV(v, angle, distance)
        #         # except:
        #         #     v = 10000
        #             # print('Complex number encountered, moving on...')
        #         # if type(item) is not complex:
        #             # if item >= 0:
        #                 # v = item
        # if len(v2) != 0:
        #     for item in v2:
        #         if item >= 0:
        #             v = item
        #             IN2 = checkValidV(v, angle, distance)
        #         # try:
        #         #     if item >= 0:
        #         #         v = item
        #         #         IN2 = checkValidV(v, angle, distance)
        #         # except:
        #         #     v = 10000
        #             # print('Complex number encountered, moving on...')
        #         # if type(item) is not complex:
        #         #     if item >= 0:
        #         #         v = item
        if IN1 or IN2:
            totalIn += 1.0

    percentIn = totalIn/(len(distances))
    print(totalIn)
    print(len(distances))
    return percentIn

def displayResults(testAngles, percentInResults):
    fig = pyplot.figure("Percent In vs Angle")
    fig.tight_layout()
    plt = fig.add_subplot(111)
    plt.set_facecolor('black')
    plt.scatter(testAngles, percentInResults, c='yellow', marker='.', alpha=0.5)
    pyplot.subplots_adjust(hspace = 0.4)
    pyplot.show()

    return

def main():
    testAngles = getAngles(p)
    testDistances = getDistances(p)

    vars = []
    for x in range(len(testAngles)):
        vars.append([testAngles[x],testDistances])

    # print(vars)
    #CHANGE PROCESSES TO HOWEVER MANY CORES U HAVE
    with Pool(processes=4, maxtasksperchild = 1) as pool:
            percentInResults = pool.map(getPercentHit, vars)
            pool.close()
            pool.join()

    displayResults(testAngles, percentInResults)

if __name__ == '__main__':
	main()

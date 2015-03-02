import numpy
__author__ = 'will'
width = 100
length = 150
heigth = 30
femurLength = 46
tibiaLength = 92


femurServoLimits = (-90, 65)
tibiaServoLimits = (-55, 90)
shoulderServoLimits = [-80, 80]

#rate to  transform pwm pulse to degrees
genericServoRate = -13.88


totalDistance = femurLength+tibiaLength


front = length/2
back = -length/2
left = width/2
right = -width/2
offset = totalDistance/3

resting_heigth = -50

legs_resting_positions = [(front+offset, left+offset, resting_heigth),
                          (front+offset, right-offset, resting_heigth),
                          (back-offset, right-offset, resting_heigth),
                          (back-offset, left+offset, resting_heigth)]    ### front left, front right, back right, back left

legs_resting_positions = numpy.array(legs_resting_positions)
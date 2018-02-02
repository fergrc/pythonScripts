"""
#############################################################################
filename    DrivingCars.py
author      Fernanda Coelho
dP email    coelho.f@digipen.edu
course      CS115
assignment  Driving Cars WIP
due date    March 15, 2017
Brief Description: Creates a Car class that imports a car geometry file 
depending on user input; positions the car and builds a motion path 
for it to follow.
#############################################################################
"""
import pymel.core as pm
import os
# import file paths for current operational system

class Car(object):
# A class that creates Car Objects)
	def __init__(self, carType, posX, posZ):
		self.carType = carType
		self.posX = posX
		self.posZ = posZ
		
		newNodes = pm.importFile(os.path.join('scenes', carType+'.ma'), rnn=1, namespace=carType)
		# rnn=1 makes it return a list of nodes
		
		# go through the node list in newNodes and look for the first transform node of the new car
		for r in newNodes:
			if r.type() == 'transform':
			# When the loop finds the first transform node, it will store it in a 'self' variable called root and break the loop	
				self.root = r
				break				
				
		r.translateX.set(posX)
		r.translateZ.set(posZ)
		
		# create empty list that buildPath() will use later to create a curve
		self.Points = []	
		# append initial car position
		self.Points.append([posX, 0, posZ]) 
		
		# create a time list that buildPath() will use later to set keys
		self.Times = []
		self.Times.append(1)
		
	def addPosition(self, x, z, t):
		# this method creates a position to the car, which can later be used by buildPath()
		self.x = x
		self.z = z
		self.t = t
		self.position = [x, 0, z]
		
		# append new time into the Times[] list
		self.Times.append(self.t)
		# append new position into the Points[] list
		self.Points.append(self.position)
		
	def buildPath(self):
		# After the user is done adding positions, they wil call the buildPath() method
		# it creates a curve with the list of positions as points.
		myPath = pm.curve(d=1, p=self.Points)
		# Now we'll constrain the car's root to the path and create a motion path animation
		motionPath = pm.pathAnimation(self.root, fractionMode=False,
    c=myPath, followAxis='z', upAxis = 'y', startTimeU=self.Times[0], endTimeU=self.Times[-1])
		
		# go through all the positions and set keys in the motion path
		for k in self.Times: # reminder to self: k is the value, and not the index of the list 
			# I will ask Python what is the index of that value and store it in a variable...
			n = self.Times.index(k)
			pm.setKeyframe(motionPath+'.uValue', v=n, t=k) # 'n' is the Uvalue position that the motionPath should be keyed at
			
c1	=	Car('Car1',	1000,	2000)	
c1.addPosition(1000,	1000,	10)

c1.addPosition(1000,	0,	20)

c1.addPosition(0,	0,	30)

c1.buildPath()


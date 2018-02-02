"""
#############################################################################
filename    bouncingBall.py
author      Fernanda Coelho
dP email    coelho.f@digipen.edu
course      CS115
assignment  Create Polygon Objects
due date    Feb 24, 2017
Brief Description:
    Function that creates an array of polygons of random size and 
	placement in the 3D space.
#############################################################################
"""

import pymel.core as pm
import random

def randPrims(numPrims, maxSize, minX, maxX, minY, maxY, minZ, maxZ, minSize=0.1): 
	prims = []
	
	for m in range(numPrims):
	# roll a random whole number between 0 to 4:
		p = random.randrange(0,5)
		if p == 0:
	# roll a random number between 0 and max sizes for all parameters
			radiusSphere = random.uniform(minSize, maxSize)
			x = random.uniform(minX, maxX)
			y = random.uniform(minY, maxY)
			z = random.uniform(minZ, maxZ)
			# store the object in a variable temporarily so it's easier to append it to the list
			n = pm.polySphere(r=radiusSphere)[0]
			pm.move(n, x, y, z)
			prims.append(n) 
		# create elif statements in case we roll 1, 2, 3 or 4
		elif p == 1:
			volCube = random.uniform(minSize, maxSize)
			x = random.uniform(minX, maxX)
			y = random.uniform(minY, maxY)
			z = random.uniform(minZ, maxZ)
			n = pm.polyCube(w=volCube, h=volCube, d=volCube)[0]
			pm.move(n, x, y, z)
			prims.append(n)
		elif p == 2:
			radiusCyl = random.uniform(minSize, maxSize)
			heightCyl = random.uniform(minSize, maxSize)
			x = random.uniform(minX, maxX)
			y = random.uniform(minY, maxY)
			z = random.uniform(minZ, maxZ)
			n = pm.polyCylinder(h=heightCyl, r=radiusCyl)[0]
			pm.move(n, x, y, z)
			prims.append(n)
		elif p == 3:
			radiusCone = random.uniform(minSize, maxSize)
			heightCone = random.uniform(minSize, maxSize)
			x = random.uniform(minX, maxX)
			y = random.uniform(minY, maxY)
			z = random.uniform(minZ, maxZ)
			n = pm.polyCone(h=heightCone, r=radiusCone)[0]
			pm.move(n, x, y, z)
			prims.append(n)
		elif p == 4:
			widthPlane = random.uniform(minSize, maxSize)
			heightPlane = random.uniform(minSize, maxSize)
			x = random.uniform(minX, maxX)
			y = random.uniform(minY, maxY)
			z = random.uniform(minZ, maxZ)
			n = pm.polyPlane(h=heightPlane, w=widthPlane)[0]
			pm.move(n, x, y, z)
			prims.append(n)
			
	return prims

randPrims(5, 5, 0, 20, 0, 5, 0, 20)

def connectPrims( a=None, b=None ):
	# if a and/or b are none, use current selection
	try:
		if a ==None or b == None:
			a = pm.selected()[0]
			b = pm.selected()[1]
	# if current selection different from 2, print error message and do nothing else
	except:
		print "Current selection must have two objects!"
	
	# have the two objects aim at each other
	global Aim1
	Aim1 = pm.aimConstraint( a, b)  
	global Aim2
	Aim2 = pm.aimConstraint( b, a)
	
	# create a curve with two points connecting the two prims
	myCurve = pm.curve(p=[(a.translate.get()), (b.translate.get())], degree=1) # creates the points at the location of the translate pivot (center of object)
	# create clusters for CVs
	cluster1 = pm.cluster(myCurve.cv[0]) # cluster for the first point of the myCurve
	cluster2 = pm.cluster(myCurve.cv[1]) # cluster for the second point of myCurve
	
	# Constrain the clusters to the points
	pm.pointConstraint( a, cluster1)
	pm.pointConstraint( b, cluster2)
	
	# rename all the objects so they relate to the their purpose
	pm.rename(a, 'ObjectA')
	pm.rename(b, 'ObjectB')
	pm.rename(Aim1, 'Aim1')
	pm.rename(Aim2, 'Aim2')
	pm.rename(myCurve, 'ConnectingLine')
	
connectPrims()

def connections():
	# create empty dictionary
	d ={}
	TargetOfAim1 = Aim1.getTargetList() # store target of aim constraints in variable
	TargetOfAim2 = Aim2.getTargetList()
	d['ObjectA'] = TargetOfAim2 # add item to d={}; key is 'ObjectA' and Value is the aim constraint target
	d['ObjectB'] = TargetOfAim1

	return d
	
connections()

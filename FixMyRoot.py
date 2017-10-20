import pymel.core as pm

# create lists for the range of the animation
animRange = []

def setRootVr(*args):
	# create variables used by functions based on user input in the UI
	global root
	root = pm.ls(sl=1)
	curRoot = str(pm.ls(os=1))
	rootNameInput.setText(curRoot)
	print 'Root has been set!'
	print root
	return

def setPelvisVr(*args):
	global pelvis
	pelvis = pm.ls(sl=1)
	curPelvis = str(pm.ls(os=1))
	hipNameInput.setText(curPelvis)
	print 'Pelvis has been set!'
	print pelvis
	return
	
def createLoc(*args):
	# create locator
	global locator
	locator = pm.spaceLocator()
	snapLoc()
	print 'Locator created and snapped to pelvis!'
	
def snapLoc():
	#snap locator to the middle of the hip and constrain
	pm.select(clear=True)
	pm.select(locator)
	pm.select(pelvis, add=True)
	pm.align(atl=True, x='Mid', y='Mid', z='Mid')
	pm.parentConstraint(pelvis, locator)
	
	return


def make_animRange():
	global startTime
	startFrame = timeInput.getValue1()
	global endFrame
	endFrame = timeInput.getValue2()
	animRange.append(startFrame)
	animRange.append(endFrame)
	# let's create a list with all the frames of our animation + inbetweens
	if endFrame != (0.0):
		currentKey = pm.currentTime(startFrame+1)
		print 'current key: ' + str(currentKey)
		animRange.append(currentKey)
		while currentKey != (endFrame-1):
			# set current time to the current key + 1, so it moves the playback to the next frame number that needs to be stored
			# in order to add that frame number to the list, we'll store it in a variable
			inbetweenFixKey = pm.currentTime(currentKey+1)
			animRange.append(inbetweenFixKey)
			# overwrite the currentKey variable so that the loop grows all the keys until it stops
			currentKey = inbetweenFixKey
		
		animRange.sort(key=int)
		# I'll sort the numbers so they'll be in the correct numeric order
		print 'All keys in the time slider:'
		print animRange
	else:
		print 'Please set a proper time range!'
		
	return

def snapRoot():
	# let's make a loop that goes through the key times and fixes the root!
	for t in animRange:
		pm.select(clear=True)
		pm.currentTime(t) # set current time to the value of the current index in the list
		pm.select(root)
		pm.select(locator, add=True)
		pm.align(atl=True, x='Mid', y='Mid') # align root to locator on the ground plane
		pm.select(clear=True)
		pm.select(root)
		pm.setKeyframe(root)
		pm.keyTangent(root, time=t, itt='linear', ott='linear', lock=False)
	
	return

def fixMyRoot(*args):
	make_animRange()
	snapRoot()
	print 'Root has been fixed!'
	return

'''UI code'''
Win = pm.window(vis=1, title='Fix My Root', s=0, h=140, w=315)
myLayout = pm.columnLayout(p=Win, adj=1)
rowLay = pm.rowLayout(p=myLayout, nc=2, adj=1)
pm.setParent(rowLay)
timeInput = pm.floatFieldGrp(nf=2, l='Start & End Frame', cl3=['center','center','center'], adj=1)
pm.setParent(myLayout)
rowLay2 = pm.rowLayout(p=myLayout, nc=3, cl2= ['center', 'center'], ad2=20)
pm.setParent(myLayout)
rootNameInput = pm.textFieldButtonGrp(adj=1, text="Click Root Control and Set", bl='Set' , columnAlign=[1, 'center'], p=myLayout, bc=setRootVr) 
hipNameInput = pm.textFieldButtonGrp(adj=1, text="Click Pelvis Control and Set", bl='Set' , columnAlign=[1, 'center'], p=myLayout, bc=setPelvisVr) 
pm.separator()
pm.button(l='Create Locator', command=createLoc)
pm.separator()
pm.button(l='Fix My Root!', command=fixMyRoot)

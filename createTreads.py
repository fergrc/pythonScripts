'''
Automates the process of connecting nodes in order to create treads for tank rigs.
by Fernanda Coelho
''' 
import pymel.core as pm

pm.currentUnit(linear='cm') # set units to cm 
treadJnts = [] # make empty list for joints that will be added later

# UI callbacks:
# function that sets the curve we're gonna use for the treads
def setCurve(*args):
	curSelCurve = pm.ls(selection=True)
	pm.rename(curSelCurve, 'treadCurve')
	curveInput.setText('Set!')

# add the selected joints to the treadJnts list created earlier
def setJntsList(*args):
	jnts = pm.ls(selection=True)
	treadJnts.extend(jnts)
	print treadJnts
	jntsInput.setText('Set!')

# if the user wishes to, they can delete the motionPaths with a UI button
def deleteMotionPaths(*args):
	try:
		for j in treadJnts:
			if('motionPath' + str(treadJnts.index(j)+1)):
				pm.delete('motionPath' + str(treadJnts.index(j)+1))
	except:
		pass

# function that makes the treads
def makeTreads(*args):
	try:
		if('world_object_up'): # if locator exists from a previous attempt, delete it
			pm.delete('world_object_up')  
			pm.spaceLocator(name='world_object_up')
			pm.addAttr(ln="Tread_Cycle", at='double', dv=0, hidden=False, k=True)
			pm.select(clear=True)
			pm.parentConstraint('treadCurve', 'world_object_up') 
	except:
		pm.spaceLocator(name='world_object_up') # or else just create it
		pm.addAttr(ln="Tread_Cycle", at='double', dv=0, hidden=False, k=True)
		pm.select(clear=True)
		pm.parentConstraint('treadCurve', 'world_object_up')
	
	try:
		for j in treadJnts: # if motionPaths exist from a previous attempt, delete them
			if('motionPath' + str(treadJnts.index(j)+1)):
				pm.delete('motionPath' + str(treadJnts.index(j)+1))
	except:
		pass
		
	# get the Max Value of the curve, so the treads loop properly
	curveMaxValue = pm.getAttr('treadCurve.maxValue')
	print curveMaxValue		 
	
	# this loop will go through each joint in the treadJnts list
	for i in treadJnts:
		# for the first joint, which has index '0'
		if treadJnts.index(str(i)) == 0:
			# select the first joint and then the curve
			pm.select(clear=True)
			pm.select(i)	
			pm.select('treadCurve', add=True)
			# constrain the first joint to the curve using motion path animation
			pm.pathAnimation(fractionMode=False, follow=True, followAxis='y', upAxis='z', worldUpType='object', worldUpObject='world_object_up', inverseUp=True, inverseFront=False, bank=False)
			# delete useless nodes we're not gonna need
			pm.delete('addDoubleLinear1', 'addDoubleLinear2', 'addDoubleLinear3','motionPath1_uValue')
			# connect motionPath allCoordinates node into the joint's translates 
			pm.connectAttr('motionPath1.allCoordinates', str(i) + '.translate', force=True) 
			# set driven keys for the anim curve driving the joints around the curve
			pm.setAttr('world_object_up.Tread_Cycle', 0) 
			pm.setAttr('motionPath1.uValue', 0)
			pm.setDrivenKeyframe('motionPath1.uValue', currentDriver='world_object_up.Tread_Cycle')
			pm.setAttr('world_object_up.Tread_Cycle', curveMaxValue)
			pm.setAttr('motionPath1.uValue', curveMaxValue)
			pm.setDrivenKeyframe('motionPath1.uValue', currentDriver='world_object_up.Tread_Cycle')
			pm.selectKey('motionPath1.uValue')
			pm.keyTangent(itt='linear', ott='linear') # make them linear and cycle
			pm.setInfinity(pri='cycle', poi='cycle')
			pm.select(clear=True)
			pm.rename('motionPath1_uValue', 'setDrivenKeys_anim_1') # rename it to something with number at the end, easier to work with if it's duplicated
			
			# for the rest of the joints:
		else: 
			# constrain the joint to the curve using motion path animation
			pm.select(clear=True)
			pm.select(i)
			pm.select('treadCurve', add=True)
			pm.pathAnimation(fractionMode=False, follow=True, followAxis='y', upAxis='z', worldUpType='object', worldUpObject='world_object_up', inverseUp=True, inverseFront=False, bank=False)
			pm.select(clear=True)
			# delete useless nodes we're not gonna need
			pm.delete('addDoubleLinear1', 'addDoubleLinear2', 'addDoubleLinear3','motionPath'+str(treadJnts.index(i)+1)+'_uValue')
			# connect motionPath allCoordinates node into joint's translates 
			pm.connectAttr('motionPath'+str(treadJnts.index(i)+1)+'.allCoordinates', str(i) + '.translate', force=True)
			pm.select(clear=True)
			# duplicate the previous set driven keys anim curve
			pm.select('setDrivenKeys_anim_'+ str(treadJnts.index(i)))
			pm.duplicate()
			pm.select(clear=True)
			# connect the new duplicated setDrivenKeys anim's output into the joint's motionPath's uValue
			pm.connectAttr('setDrivenKeys_anim_'+str(treadJnts.index(i)+1)+'.output', 'motionPath'+str(treadJnts.index(i)+1)+'.uValue', force=True)
			# connect the animation curve to the Tread Cycle attribute
			pm.connectAttr('world_object_up.Tread_Cycle', 'setDrivenKeys_anim_'+str(treadJnts.index(i)+1)+'.input', force=True)
			# shift the animation curve to the side so the treads won't be on top of each other and move accordingly 
			pm.select('setDrivenKeys_anim_'+str(treadJnts.index(i)+1))
			pm.selectKey()
			num = spaceInput.getValue1() # get the spacing the user wants
			pm.keyframe(option='over', relative=True, floatChange=(num))
			pm.select(clear=True)
		
#################################################################################################
# UI CODE

# if UI window already exists, kill it
try:
	pm.window('Create Treads', exists = True)
	pm.deleteUI(winUI)
except:
	pass

# create window with widgets
winUI = pm.window('Create Treads', s=0, h=150)
pm.showWindow(winUI)
column = pm.columnLayout()
curveInput = pm.textFieldButtonGrp(text="Click Curve and Set", bl='Set' ,  p=column, bc=setCurve) 
jntsInput = pm.textFieldButtonGrp(text="Select Tread jnts and Set", bl='Set' , p=column, bc=setJntsList) 
spaceInput = pm.floatFieldGrp(nf=1, l='Offset',p=column, precision=3)
makeTreadsButton = pm.button(l='Make Treads', p=column, c=makeTreads)
deleteMotionPaths = pm.button(l='Delete Motion Paths', p=column, c=deleteMotionPaths)

#################################################################################################

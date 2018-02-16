'''
Script to create stretchy tentacles.
by Fernanda Coelho
'''

import pymel.core as pm
joints = []

# function that puts the joints we're working with in a list
def createJntsList(*args):
	jnts = pm.ls(selection=True)
	joints.extend(jnts)
	print joints

print
# function that makes all the nodes for us
def makeMyNodes(*args):
	prefix = prefixInput.getText() # gets the user's prefix to the nodes for a tentacle
	# Create CurveInfo node
	pm.shadingNode('curveInfo', asUtility=True, name=prefix+'_CurveInfo') 
	# Connect tentacle1_spline_IK_curveShape.WorldSpace into CurveInfo.InputCurve
	pm.connectAttr(prefix+'_spline_IK_curveShape.worldSpace', prefix+'_CurveInfo.inputCurve')
	# Create multiplyDivide node, rename it "DivideZScale"
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_DivideZScale') 
	# Connect CurveInfo.arcLenght into DivideZScale>input1>input1X
	pm.connectAttr(prefix+'_CurveInfo.arcLength', prefix+'_DivideZScale.input1.input1X')
	# In DivideZScale node attributes, copy original Input 1x into Input 2x, change operation to Divide
	pm.setAttr(prefix+'_DivideZScale.operation', 2)
	pm.setAttr (prefix+'_DivideZScale.input2X', 9.5)
	# DivideZScale.OutputX into Scale Z in each Joint
	for j in joints:
		pm.connectAttr(prefix+'_DivideZScale.output.outputX', str(j) + '.scale.scaleZ')
	# Create another multiplyDivide node and rename it
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_POW_ZY') 
	# Connect DivideZScale.OutputX into new POW_ZY.input1X
	pm.connectAttr(prefix+'_DivideZScale.output.outputX', prefix+'_POW_ZY.input1.input1X')
	# Change operation to power, and input2X to 0.5
	pm.setAttr(prefix+'_POW_ZY.operation', 3)
	pm.setAttr (prefix+'_POW_ZY.input2X', 0.5)
	# Create another multiplyDivide node, rename it "stretch_invert_DIV"
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_stretch_invert_DIV')
	# Connect POW_ZY.outputX into stretch_invert_DIV.input2X
	pm.connectAttr(prefix+'_POW_ZY.output.outputX', prefix+'_stretch_invert_DIV.input2.input2X')
	# Set operation of stretch_invert_DIV to Divide and inputX to 1
	pm.setAttr(prefix+'_stretch_invert_DIV.operation', 2)
	pm.setAttr (prefix+'_stretch_invert_DIV.input1X', 1)
	
	# In the connection editor, connect stretch_invert_DIV.outputX into the tentacle joints.scaleX and scaleY
	for j in joints:
		pm.connectAttr(prefix+'_stretch_invert_DIV.output.outputX', str(j)+'.scale.scaleX')
		pm.connectAttr(prefix+'_stretch_invert_DIV.output.outputX', str(j)+'.scale.scaleY')
		
#################################################################################################
# UI CODE

# if UI window already exists, kill it
try:
	pm.window('Create Stretch', exists = True)
	pm.deleteUI(winUI)
except:
	pass
# create window with widgets
winUI = pm.window('Create Stretch', s=False, h=80, w= 80)
pm.showWindow(winUI)
column = pm.columnLayout()
prefixInput = pm.textField(p=column, text='prefix')
jntsInput = pm.button(l='Set Jnts', p=column, c=createJntsList)
makeTreadsButton = pm.button(l='do it', p=column, c=makeMyNodes)

#################################################################################################

import pymel.core as pm

# function that makes all the nodes for us
def makeMyNodes(crve, prefix, downAxis, sideAxis1, sideAxis2):
	# Create CurveInfo node
	pm.shadingNode('curveInfo', asUtility=True, name=prefix+'_CurveInfo') 
	# Connect curve worldspace into CurveInfo
	pm.connectAttr(crve+'Shape.worldSpace', prefix+'_CurveInfo.inputCurve')
    # get original lenght of the curve
	ogLnght = pm.getAttr(prefix+'_CurveInfo.arcLength')
	# Create multiplyDivide node, rename it "DivideZScale"
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_DivideZScale') 
	# Connect CurveInfo.arcLenght into DivideZScale>input1>input1X
	pm.connectAttr(prefix+'_CurveInfo.arcLength', prefix+'_DivideZScale.input1.input1X')
	# In DivideZScale node attributes, copy original Input 1x into Input 2x, change operation to Divide
	pm.setAttr(prefix+'_DivideZScale.operation', 2)
	pm.setAttr (prefix+'_DivideZScale.input2X', ogLnght)
	# DivideZScale.OutputX into Scale Z in each Joint

	for j in jnts:
		pm.connectAttr(prefix+'_DivideZScale.output.outputX', str(j) + '.scale.scale'+downAxis)
	# Create another multiplyDivide node and rename it
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_POW_ZY') 
	# Connect DivideZScale.OutputX into new POW_ZY.input1X
	pm.connectAttr(prefix+'_DivideZScale.output.outputX', prefix+'_POW_ZY.input1.input1X')
	# Change operation to power, and input2X to 0.5
	pm.setAttr(prefix+'_POW_ZY.operation', 3)
	pm.setAttr (prefix+'_POW_ZY.input2X', -1)
	# Create another multiplyDivide node, rename it "stretch_invert_DIV"
	pm.shadingNode('multiplyDivide', asUtility=True, name=prefix+'_stretch_invert_DIV')
	# Connect POW_ZY.outputX into stretch_invert_DIV.input2X
	pm.connectAttr(prefix+'_POW_ZY.output.outputX', prefix+'_stretch_invert_DIV.input2.input2X')
	# Set operation of stretch_invert_DIV to Divide and inputX to 1
	pm.setAttr(prefix+'_stretch_invert_DIV.operation', 2)
	pm.setAttr (prefix+'_stretch_invert_DIV.input1X', 1)

	# In the connection editor, connect stretch_invert_DIV.outputX into the tentacle joints.scales
	for j in jnts:
		pm.connectAttr(prefix+'_stretch_invert_DIV.output.outputX', str(j)+'.scale.scale'+sideAxis1)
		pm.connectAttr(prefix+'_stretch_invert_DIV.output.outputX', str(j)+'.scale.scale'+sideAxis2)
 
'''
# Get joints from selection
jnts = pm.ls(selection=True)

makeMyNodes(crve, prefix, downAxis, sideAxis1, sideAxis2)
'''

"""
#############################################################################
filename    bouncingBall.py
author      Fernanda Coelho
dP email    coelho.f@digipen.edu
course      CS115A
assignment  A1 - Bouncing Ball
due date    Feb 6st, 2017
Brief Description:
    Final code for a 24 frame bouncing ball cycle.
#############################################################################
"""

import pymel.core as pm
# create a sphere of any radius, store it in a variable called "ball" then rename it "ball" in the outliner
ballRadius = 2
b1 = pm.polySphere(r=ballRadius)[0]
pm.rename(b1, 'ball')
# move the pivot point to the bottom of the object
# Khan notes: we need to move both the scalePivot and the rotatePivot, Maya doesn't have a translate pivot 
pm.move(0, -1 * ballRadius, 0, b1.scalePivot, b1.rotatePivot)
# place the ball on top of the grid (pivot point touching the grid) and use it as a ground plane
pm.move(0, ballRadius, 0)
# freeze transformations on the ball so it won't clip through the ground plane when we translate it down
pm.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

def bounceOnce(ball, firstFrame, height, squash, decay):
	# this function defines the keys for a 24 frame bouncing ball of any size
	# top of bounce:
	pm.currentTime(firstFrame)
	ball.scaleX.set(1)
	ball.scaleY.set(1)
	ball.scaleZ.set(1)
	ball.translateY.set(height)
	pm.setKeyframe(ball)
	pm.keyTangent(ball.translateY, time=firstFrame, itt='auto', ott='auto', lock=False)
	
	# bottom of bounce
	# contact key
	pm.currentTime(firstFrame + 11)
	ball.scaleX.set(1)
	ball.scaleY.set(1+(1-squash))
	ball.scaleZ.set(1)
	ball.translateY.set(0)
	pm.setKeyframe(ball)
	pm.keyTangent(ball.translateY, time=firstFrame + 11, itt='linear', ott='linear', lock=False)
	pm.keyTangent(ball.scaleY, time=firstFrame + 11, itt='linear', ott='step', lock=False)
	
	# create a squash key
	pm.currentTime(firstFrame + 12)
	ball.scaleX.set(1)
	ball.scaleY.set(squash)
	ball.scaleZ.set(1)
	ball.translateY.set(0)
	pm.setKeyframe(ball)
	pm.keyTangent(ball.translateY, time=firstFrame + 12, itt='linear', ott='linear', lock=False)
	
	pm.currentTime(firstFrame + 24)
	ball.scaleX.set(1)
	ball.scaleY.set(1)
	ball.scaleZ.set(1)
	ball.translateY.set(height)
	pm.setKeyframe(ball)
	pm.keyTangent(ball.translateY, time=firstFrame+24, itt='auto', ott='auto', lock=False)
	

	return

# let's call the function more than once
height = 10
decay = 0.8
# note: squash must be a value between 0 and 1
squash = 0.6

for bounce in range(6):
	bounceOnce(b1, bounce*24 + 1, height, squash, decay)
	# same as height = height * decay
	# the decay will only start taking place after the ball bounce for the fist time, so the first bounce will have its normal height 
	height *= decay
	squash += 0.1
	if squash > 1:
		squash = 1
	
	if b1.translateY.get < 1:
		break
	
	# let's make sure the ball's last position is at the ground plane instead of the apex
	pm.currentTime( query=True )
	b1.scaleX.set(1)
	b1.scaleY.set(1)
	b1.scaleZ.set(1)
	b1.translateY.set(0)

	

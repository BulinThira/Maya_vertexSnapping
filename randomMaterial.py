# randomMaterial.py - Python Script

# DESCRIPTION: Tool for assigning random materials
# REQUIRE: Python3
# AUTHOR: BulinThira - Github

import maya.cmds as mc
import random
import math

#UI

def matRand():
    if mc.window('matRand_window', q=True, ex=True):
        mc.deleteUI('matRand_window', window=True)
    mc.window('matRand_window', title='Random Materials')
    mc.columnLayout(adj=True)
    
    mc.frameLayout(label='Choose material as choices', bgc=(0.1, 0.5, 0.5))
    
    mc.button(label='Bake Materials', h=30, c=bakeMat)
    
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Materials >> ')
    mc.text('result_mat', label='')
    mc.setParent('..')
    
    mc.button(label='Bake Objects', h=30, c=bakeObj)
    
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Object count >> ')
    mc.text('result_obj', label='')
    mc.setParent('..')
    
    mc.button(label='Assign Random Material', h=30, c=doRandMat)
    
    
    mc.showWindow('matRand_window')
    mc.window('matRand_window', e=True, wh=(300,180))
    
#functions
 
objSelected = []
matSelected = []


def bakeMat(*args):
    matCnt = mc.ls(sl=True)
    del matSelected[:]
    for each in matCnt:
        matSelected.append(each)
    resultText = (f'{matSelected}')
    print(resultText)
    mc.text('result_mat', e=True, label=resultText)
    
def bakeObj(*args):
    objCnt = mc.ls(sl=True)
    del objSelected[:]
    for each in objCnt:
        objSelected.append(each)
    resultText_obj = (f'{objSelected}')
    print(resultText_obj)
    mc.text('result_obj', e=True, label=resultText_obj)

def doRandMat(*args):
	matCount = len(matSelected)
	for each in objSelected:
		randNum = random.random()
		turnNum = math.floor(randNum*(matCount))
		intNum = int(turnNum)
		mc.select(each)
		matName = matSelected[intNum]
		mc.hyperShade(assign=matName)
	mc.select(clear=True)

    
matRand()
# vertexSnapping.py - Python Script

# DESCRIPTION: Tool for creating primitive objects on sorce object's vertexs
# REQUIRE: Python3
# AUTHOR: BulinThira - Github

import maya.cmds as mc
import random

def snapObj():
    if mc.window('snapObj_window', q=True, ex=True):
        mc.deleteUI('snapObj_window', window=True)
    mc.window('snapObj_window', title='Vertex Snapping')
    mc.columnLayout(adj=True)
    
    mc.rowLayout(numberOfColumns=3)
    mc.text(label='source')
    mc.textField('src_TF', w=150)
    mc.button(label='Get', w=80, c=GetSrcBut)
    mc.setParent('..')
    
    mc.rowLayout(numberOfColumns=3)
    mc.optionMenu('optionprim', label='Primitives')
    mc.menuItem ('sphere')
    mc.menuItem ('cube')
    mc.menuItem ('cone')
    mc.menuItem ('plane')
    mc.setParent('..')
    
    
    
    #transform slider#

    mc.frameLayout(label='Offset', bgc=(0.1, 0.5, 0.5))
    
    mc.rowLayout(numberOfColumns = 2)
    mc.text(label='rotate')
    mc.setParent( '..' )
    
    mc.rowLayout(numberOfColumns = 2)
    mc.floatSliderGrp('rmin_floatSliderGrp', label='min', field=True, min=0.0, max=360)
    mc.floatSliderGrp('rmax_floatSliderGrp', label='max', field=True, min=0.0, max=360)
    mc.setParent( '..' )
    
    mc.rowLayout(numberOfColumns = 2)
    mc.text(label='scale')
    mc.setParent( '..' )
    
    mc.rowLayout(numberOfColumns = 2)
    mc.floatSliderGrp('smin_floatSliderGrp', label='min', field=True, min=0.0, max=5.0)
    mc.floatSliderGrp('smax_floatSliderGrp', label='max', field=True, min=0.0, max=5.0)
    mc.setParent( '..' )
    
    mc.button(label='Generate', h=30, c=doCreate)
    
    
    mc.showWindow('snapObj_window')
    mc.window('snapObj_window', e=True, wh=(800,210))
    
def GetSrcBut(*args):
    sels = mc.ls(sl=True)
    
    if sels:
        mc.textField('src_TF', e=True, tx=sels[0])
    else:
        mc.textField('src_TF', e=True, tx='')
        
def GetPrtBut(*args):
    sels = mc.ls(sl=True)
    
    if sels:
        mc.textField('prt_TF', e=True, tx=sels[0])
    else:
        mc.textField('prt_TF', e=True, tx='')
        
    
def doCreate(*args):
    src_sel = mc.textField('src_TF', q=True, tx=True)
    prim_sel = mc.optionMenu('optionprim', q=True, v=True)
    RMIN = mc.floatSliderGrp('rmin_floatSliderGrp', q=True, v=True)
    RMAX = mc.floatSliderGrp('rmax_floatSliderGrp', q=True, v=True)
    SMIN = mc.floatSliderGrp('smin_floatSliderGrp', q=True, v=True)
    SMAX = mc.floatSliderGrp('smax_floatSliderGrp', q=True, v=True)
    snapObject(src_sel, prim_sel, RMIN, RMAX, SMIN, SMAX)
    
    
def snapObject(source, primitive, r_min, r_max, s_min, s_max):
    vtx_count = mc.polyEvaluate(source, v=True)
    objs = []
    
    amp = 2
    inc = 1
    
    for i in range(vtx_count):
        vtx_id = f'{source}.vtx[{i}]'
        pos = mc.xform(vtx_id, q=True, t=True, ws=True)
        obj = ''

        if primitive == 'sphere':
            obj = mc.polySphere(ch=False)[0]
                    
        elif primitive == 'cube':
            obj = mc.polyCube(ch=False)[0]
                    
        elif primitive == 'cone':
            obj = mc.polyCone(ch=False)[0]
                    
        elif primitive == 'plane':
            obj = mc.polyPlane(ch=False)[0]
                    
     
        objs.append(obj)

        offset = (((vtx_count-1)*amp)/2)*-1
                
        cmds.xform(obj, t=pos,
                        s = [random.uniform(s_min, s_max),
                                random.uniform(s_min, s_max),
                                random.uniform(s_min, s_max)],
                                        
                        ro = [random.uniform(r_min, r_max),
                                random.uniform(r_min, r_max),
                                random.uniform(r_min, r_max)])
        inc += 1
    cmds.group(objs, name = 'prims_Grp')
        

    
snapObj()
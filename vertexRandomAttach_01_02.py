import maya.cmds as cmds
import random

"""

        Script for attaching secondary object to the main object

"""

def objectVertexAttach():

    # reate UI window #

    if cmds.window("objectVertexAttach_window", q=True, exists=True):
        cmds.deleteUI("objectVertexAttach_window", window=True)

    cmds.window(
        "objectVertexAttach_window",
        title="Object Vertex Attach"
    )
    cmds.columnLayout(adjustableColumn=True)

    cmds.rowLayout(numberOfColumns=3)
    cmds.text(label="Source Object: ")
    cmds.textField("src_tf", width=80)
    cmds.button(label="get", width=25, command=bakeSourceObject)
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Vertex Count >> ")
    cmds.text("vtxCnt", label="")
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=3)
    cmds.text(label="Sub Object: ")
    cmds.textField("sub_tf", width=80)
    cmds.button(label="get", width=25, command=bakeSubObject)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Random Vertex Count: ")
    cmds.intField("randomVertexCount_textField", width=80, minValue=1)
    cmds.setParent("..")

    # rotation slider #

    cmds.frameLayout(label="Rotate Offset", backgroundColor=(0.1, 0.5, 0.5))

    wrapUI_offset(offsetType="rotateX", minMaxType="rx", minFloat=0.0, maxFloat=360)
    wrapUI_offset(offsetType="rotateY", minMaxType="ry", minFloat=0.0, maxFloat=360)
    wrapUI_offset(offsetType="rotateZ", minMaxType="rz", minFloat=0.0, maxFloat=360)

    # scale slider #

    cmds.frameLayout(label="Scale Offset", backgroundColor=(0.1, 0.5, 0.5))

    wrapUI_offset(offsetType="scaleX", minMaxType="sx", minFloat=0.0, maxFloat=10)
    wrapUI_offset(offsetType="scaleY", minMaxType="sy", minFloat=0.0, maxFloat=10)
    wrapUI_offset(offsetType="scaleZ", minMaxType="sz", minFloat=0.0, maxFloat=10)

    cmds.button(label="generate", command=subObjectAttach)

    cmds.showWindow("objectVertexAttach_window")
    cmds.window("objectVertexAttach_window", e=True, widthHeight=(900, 480))


def wrapUI_offset(offsetType="", minMaxType="", minFloat=1, maxFloat=1):

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label=offsetType)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2)
    cmds.floatSliderGrp(
        "{min_kw}min_floatSliderGrp".format(min_kw=minMaxType),
        label="min",
        field=True,
        min=minFloat,
        max=maxFloat,
    )
    cmds.floatSliderGrp(
        "{max_kw}max_floatSliderGrp".format(max_kw=minMaxType),
        label="max",
        field=True,
        min=minFloat,
        max=maxFloat,
    )
    cmds.setParent("..")
def bakeSourceObject(sourceObject=""):
    sels = cmds.ls(sl=True)
    vtx_count = cmds.polyEvaluate(sels, v=True)

    if sels:
        cmds.textField("src_tf", e=True, tx=sels[0])
        cmds.text("vtxCnt", e=True, label=vtx_count)
    else:
        cmds.textField("src_tf", e=True, tx="")
        cmds.text("vtxCnt", e=True, label="INVALID")


def bakeSubObject(subObject=""):
    sels = cmds.ls(sl=True)

    if sels:
        cmds.textField("sub_tf", e=True, tx=sels[0])
    else:
        cmds.textField("sub_tf", e=True, tx="")


def subObjectAttach(*arg):
    source = cmds.textField("src_tf", q=True, tx=True)
    sub = cmds.textField("sub_tf", q=True, tx=True)
    randomVertexCount = cmds.intField("randomVertexCount_textField", q=True, v=True)

    rx_min = cmds.floatSliderGrp("rxmin_floatSliderGrp", q=True, v=True)
    ry_min = cmds.floatSliderGrp("rymin_floatSliderGrp", q=True, v=True)
    rz_min = cmds.floatSliderGrp("rzmin_floatSliderGrp", q=True, v=True)

    rx_max = cmds.floatSliderGrp("rxmax_floatSliderGrp", q=True, v=True)
    ry_max = cmds.floatSliderGrp("rymax_floatSliderGrp", q=True, v=True)
    rz_max = cmds.floatSliderGrp("rzmax_floatSliderGrp", q=True, v=True)

    sx_min = cmds.floatSliderGrp("sxmin_floatSliderGrp", q=True, v=True)
    sy_min = cmds.floatSliderGrp("symin_floatSliderGrp", q=True, v=True)
    sz_min = cmds.floatSliderGrp("szmin_floatSliderGrp", q=True, v=True)

    sx_max = cmds.floatSliderGrp("sxmax_floatSliderGrp", q=True, v=True)
    sy_max = cmds.floatSliderGrp("symax_floatSliderGrp", q=True, v=True)
    sz_max = cmds.floatSliderGrp("szmax_floatSliderGrp", q=True, v=True)

    vertexCount = cmds.polyEvaluate(source, v=True)
    cmds.group(em=True, name="{source_kw}_dup_grp".format(source_kw=source))

    objectCount = 1
    existVertex = []
    idRandomizer = 0
    
    for i in range(randomVertexCount):
        
        idRandomizer = random.randint(randomVertexCount, vertexCount)
        while idRandomizer not in existVertex:
            existVertex.append(idRandomizer)
                
            vtx_id = "{source_kw}.vtx[{i_kw}]".format(
                source_kw=source, i_kw=idRandomizer
            )
    
            ### not include already attached vertex
    
            pos = cmds.xform(vtx_id, q=True, translation=True, worldSpace=True)
    
            obj = ""
            
            #print(idRandomizer)
            
            
            obj = cmds.duplicate(
                "{sub_kw}".format(sub_kw=sub),
                n="{sub_kw}_duplicate_{pad_kw}".format(
                    pad_kw=str(objectCount).zfill(4), sub_kw=sub
                ),
            )
            cmds.xform(
                obj,
                t=pos,
                s=[
                    random.uniform(sx_min, sx_max),
                    random.uniform(sy_min, sy_max),
                    random.uniform(sz_min, sz_max),
                ],
                ro=[
                    random.uniform(rx_min, rx_max),
                    random.uniform(ry_min, ry_max),
                    random.uniform(rz_min, rz_max),
                ],
            )

        cmds.parent(obj, "{source_kw}_dup_grp".format(source_kw=source))
        objectCount += 1
    print(existVertex)


objectVertexAttach()
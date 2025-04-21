import maya.cmds as cmds
import maya.mel as mel

import sys
import importlib

# Ensure the directory is in sys.path
if "C:/maya_scripts" not in sys.path:
    sys.path.append("E:\GitHub\MayaTools\MikModRig")

import MMRCurveLibrary as mmrcl

importlib.reload(mmrcl)
import MMRCurveLibrary as mmrcl

from MmrSettings import MmrSettings as mmrs
import MmrHelpers as mmrh

def makeFkCtrls(ctrlFunc=mmrcl.circle, size=1):
    selJntList = cmds.ls(sl=True, type='joint')
    for jnt in selJntList:
        print(jnt)
        cls.makeFkCtrl(ctrlFunc, jnt=jnt, size=size)

def makeFkCtrl(ctrlFunc=mmrcl.circle, jnt='', size=1):

    # parent constrains a group containing a nurbs circle at each of the joints selected, deletes the constraint.
    # Good for setting up control objects for FK    
    # if a non-joint object is part of the selected list (last one will be used), it will use a duplicate of this type of object    
    # as the control object == otherwise, a circle NOTE: this does not seem to work well with branching heirarchies
    
    # set this to whatever you want removed at the end of the joint names for control and group naming
    # make a ctrl object of type ctrlObj  
    nameBud = jnt[:-len(mmrs.JNT_SUFFIX)]
        
    ctrlObj = ctrlFunc(name=f'{nameBud}{mmrs.CTRL_SUFFIX}', size=size)   
    # group it with similar name        
    grp = cmds.group(ctrlObj,n=f'{nameBud}{mmrs.GRP_SUFFIX}')       
    # parent constrain the grp to the joint to get rotations        
    cmds.parentConstraint(jnt,grp,mo=False)        
    # remove parent constraint        
    x = cmds.listRelatives(grp,type='constraint')       
    cmds.delete(x)
        
def make_ik_fk_arm(prefix):
    # Get selected joints
    selection = cmds.ls(selection=True)
    startJnt = selection[0]
    endJnt = selection[1]
    
    # Temporarily unparent children of end joint
    children = cmds.listRelatives(endJnt, children=True)
    for child in children:
        cmds.parent(child, world=True)
    
    # Create IK FK GRP
    cmds.select(clear=True)
    ikFkGrp = cmds.group(name=f'{prefix}_arm_IK_FK_GRP', empty=True, world=True)
    
    # Create FK JNTs
    fkJnts = cmds.duplicate(startJnt)
    cmds.parent(fkJnts[0], ikFkGrp)
    cmds.select(fkJnts[0])
    cmds.rename(fkJnts[0], fkJnts[0][:-1])
    mel.eval('searchReplaceNames "JNT" "FK_JNT" "hierarchy"')
    
    # Create IK JNTs
    ikJnts = cmds.duplicate(startJnt)
    cmds.parent(ikJnts[0], ikFkGrp)
    cmds.select(ikJnts[0])
    cmds.rename(ikJnts[0], ikJnts[0][:-1])
    mel.eval('searchReplaceNames "JNT" "IK_JNT" "hierarchy"')
    
    # Reparent children of end joint
    for child in children:
        cmds.parent(child, endJnt)
    
    
#makeFkCtrls(mmrcl.cube, size = 2)

make_ik_fk_arm('L')
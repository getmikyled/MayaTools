import maya.cmds as cmds
import maya.mel as mel

from curve_library import CurveLibrary
from auto_rig_helpers import AutoRigHelpers
        
class BallAutoRig(object):
    
    def __init__(self):
        self.primary_color = [0.0, 0.0, 1.0]
        self.secondary_color = [1.0, 1.0, 1.0]
        
    def set_colors(self, primary, secondary):
        self.primary_color = primary
        self.secondary_color = secondary
        
        
    # Construct ball rig
    def construct_rig(self, name="ball"):
        cmds.select(clear=True)
        
        # Create groups 
        root_grp = cmds.group(name=name, empty=True, world=True)
        anim_ctrls_grp = cmds.group(name="anim_controls", empty=True, parent=root_grp)
        geometry_grp = cmds.group(name="geometry_DoNotTouch", empty=True, parent=root_grp)
        
        # Create ball geometry and control
        ball_geo = self.create_ball("ball_geo", geometry_grp)
        ball_ctrl = self.create_ball_ctrl("ball_ctrl", parent=anim_ctrls_grp)
        
        # Create squash control
        squash_grp = cmds.group(name="squash_grp", empty=True, parent=anim_ctrls_grp)
        squash_ctrl = self.create_squash_ctrl(name="squash_ctrl", parent=squash_grp)
        cmds.pointConstraint(ball_ctrl, squash_grp, offset=[0,0,0], weight=1)
        
        # Constraint: Ball Geo -> Ball Ctrl
        cmds.parentConstraint(ball_ctrl, ball_geo, maintainOffset=True, weight=1)
        
        self.create_squash_deformer(ball_geo, squash_ctrl)
        
        # Create display layer to make ball geo a reference (Not selectable)
        AutoRigHelpers.create_display_layer("ball_geometry", [ball_geo], True)
        
    # Create ball geometry
    def create_ball(self, name, parent=None):
        ball_geo = cmds.sphere(pivot=(0,0,0), axis=(0,1,0), radius=1, name=name)[0]
        if parent:
            ball_geo = cmds.parent(ball_geo, parent)[0]
            
        # Create ball shader and assign it to ball geo
        self.create_ball_shader(ball_geo)

        return ball_geo
                
    def create_ball_ctrl(self, name, parent=None):
        # Create NURB Circle for ball_Ctrl
        ball_ctrl = CurveLibrary.two_way_arrow(name=name)
        
        # Parent ball_ctrl accordingly
        if parent:
            ball_ctrl = cmds.parent(ball_ctrl, parent)[0]
            
        # Lock and Hide necessary attributes
        AutoRigHelpers.lock_hide_attrs(ball_ctrl, ["sx", "sy", "sz", "v"])
        
        # Modify rotation order
        AutoRigHelpers.set_attr(ball_ctrl, "rotateOrder", 3)
            
        return ball_ctrl
        
    def create_ball_shader(self, ball_geo):
        ball_shape = AutoRigHelpers.get_shape_from_transform(ball_geo)
        ball_shader = AutoRigHelpers.create_assign_lambert_shader("ballShader", ball_shape)
        
        # Create Ramp Node & place2DTexture
        ramp = cmds.shadingNode("ramp", name="ballRamp", asTexture=True)
        place2dTexture = cmds.shadingNode("place2dTexture", name="ballPlace2dTexture", asUtility=True)
        AutoRigHelpers.connect_attr(place2dTexture, "outUV", ramp, "uv")
        AutoRigHelpers.connect_attr(place2dTexture, "outUvFilterSize", ramp, "uvFilterSize")
        AutoRigHelpers.connect_attr(ramp, "outColor", ball_shader, "color")
        
        # Set Ramp Node Colors & place2DTexture repeats
        AutoRigHelpers.set_attr(ramp, "interpolation", 0)
        AutoRigHelpers.set_attr(ramp, "colorEntryList[0].position", 0)
        AutoRigHelpers.set_attr(ramp, "colorEntryList[0].color", self.primary_color, "double3")
        AutoRigHelpers.set_attr(ramp, "colorEntryList[1].position", 0.5)
        AutoRigHelpers.set_attr(ramp, "colorEntryList[1].color", self.secondary_color, "double3")
        AutoRigHelpers.set_attr(place2dTexture, "repeatU", 1)
        AutoRigHelpers.set_attr(place2dTexture, "repeatV", 3)
        
    def create_squash_ctrl(self, name, parent=None):
        squash_ctrl = CurveLibrary.disc(radius=1.6, name=name)
        if parent:
            squash_ctrl = cmds.parent(squash_ctrl, parent)[0]
        
        AutoRigHelpers.lock_hide_attrs(squash_ctrl, ["sx", "sy", "sz", "v"])
        AutoRigHelpers.add_attr(squash_ctrl, "squashStretch", "double", 0, keyable=True)
        
        # Set rotate order to 'xzy'
        AutoRigHelpers.set_attr(squash_ctrl, "rotateOrder", 3)
        
        return squash_ctrl
        
    def create_squash_deformer(self, squash_obj, squash_ctrl):
        # Replace current selection with squash object
        cmds.select(squash_obj, replace=True)
        cmds.Squash()
        
        # Get squash handle and deformer using selection
        squash_handle, squash_deformer = cmds.ls(sl=True, long=True)
        squash_handle = cmds.rename(squash_handle, "ball_squash")
        
        # Lock and hide squash handle visibility
        AutoRigHelpers.set_attr(squash_handle, "visibility", False)
        AutoRigHelpers.lock_hide_attrs(squash_handle, ["v"], hide=False)
        
        cmds.parent(squash_handle, squash_ctrl)
        
        # Connect squashStretch attribute to deformer
        AutoRigHelpers.connect_attr(squash_ctrl, "squashStretch", squash_deformer, "factor", force=True)
        
        # Clear selection
        cmds.select(clear=True)
        
if __name__ == "__main__":
    cmds.file(newFile=True, force=True)
    
    ballRig = BallAutoRig()
    ballRig.construct_rig()
    
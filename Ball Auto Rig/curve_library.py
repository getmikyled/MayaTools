import maya.cmds as cmds

from auto_rig_helpers import AutoRigHelpers

class CurveLibrary(object):
    
    @classmethod
    def circle(cls, radius=1, name="circle_curve"):
        return cmds.circle(center=(0,0,0), normal=(0,1,0), radius=radius, name=name)[0]
        
    @classmethod
    def two_way_arrow(cls, name="two_way_arrow_crv"):
        return cmds.curve(degree=1,
                          point=[(-1,0,-2),(-2,0,-2),(0,0,-4),(2,0,-2),(1,0,-2),(1,0,2),(2,0,2),(0,0,4),(-2,0,2),(-1,0,2),(-1,0,-2)],
                          knot=[0,1,2,3,4,5,6,7,8,9,10],
                          name=name)
                          
    @classmethod
    def disc(cls, radius=2, name="disc"):
        # Create inner/outer circle and mark as unselectable
        outer_circle = cls.circle(radius=radius, name="outer_circle_crv")
        AutoRigHelpers.make_unselectable(outer_circle)
        inner_circle = cls.circle(radius=radius*0.1, name="inner_circle_crv")
        AutoRigHelpers.make_unselectable(inner_circle)      
    
        disc_geo = cmds.loft(outer_circle, inner_circle, uniform=True, ar=True, po=False, rsn=True, name=name)[0]
        outer_circle, inner_circle = cmds.parent(outer_circle, inner_circle, disc_geo)
        
        # Delete construction history
        cmds.delete(outer_circle, inner_circle, disc_geo, ch=True)
        
        # Create and assign disc shader
        disc_geo_shape = AutoRigHelpers.get_shape_from_transform(disc_geo)
        disc_shader = AutoRigHelpers.create_assign_lambert_shader("dischader", disc_geo_shape)
        AutoRigHelpers.set_attr(disc_shader, "color", [0.6, 0.6, 0.6], value_type="double3")
        AutoRigHelpers.set_attr(disc_shader, "transparency", [0.75, 0.75, 0.75], value_type="double3")
        
        # Parent circles to disc_geo
        return disc_geo
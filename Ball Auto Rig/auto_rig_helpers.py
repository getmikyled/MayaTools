import maya.cmds as cmds

def get_attr(node, attr):
    return cmds.getAttr("{0}.{1}".format(node, attr))

def add_attr(node, long_name, attr_type, default_value, keyable=False):
    cmds.addAttr(node, longName=long_name, attributeType=attr_type, defaultValue=default_value, keyable=keyable)
    
def set_attr(node, attr, value, value_type=None):
    if value_type:
        # If type is a list, unpack it for setting attributes w/ multiple values
        cmds.setAttr("{0}.{1}".format(node, attr), *value, type=value_type)
    else:
        # If attribute is being set with only one value
        cmds.setAttr("{0}.{1}".format(node, attr), value)
        
def connect_attr(node_a, attr_a, node_b, attr_b, force=False):
    # Connect attribute in node a to attribute in node b
    cmds.connectAttr("{0}.{1}".format(node_a, attr_a), "{0}.{1}".format(node_b, attr_b), force=force)
    
def lock_hide_attrs(node, attrs, lock=True, hide=True, channelBox=False):
    # if hide is true, the attr should NOT be keyable
    keyable = not hide
    
    # lock/hide all attrs in node
    for attr in attrs:
        full_reference = "{0}.{1}".format(node, attr)
        cmds.setAttr(full_reference, lock=lock, keyable=keyable, channelBox=channelBox)
        
def create_display_layer(name, members, reference=False):
    # Create display layer
    display_layer = cmds.createDisplayLayer(name=name, empty=True)
    
    # Set layer as reference if true
    if reference:
        cmds.setAttr("{0}.displayType".format(display_layer), 2)
        
    # Add members to layer if provided
    if members:
        cmds.editDisplayLayerMembers(display_layer, members, noRecurse=True)
        
    return display_layer
    
def create_assign_lambert_shader(name, shape_node):
    # Create shader
    shader = cmds.shadingNode("lambert", name=name, asShader=True)
    shader_sg = cmds.sets(name="{0}SG".format(shader), renderable=True, noSurfaceShader=True, empty=True)
    cls.connect_attr(shader, "outColor", shader_sg, "surfaceShader")
    
    # Assign shader to shape node
    cmds.sets([shape_node], e=True, forceElement=shader_sg)
    
    return shader

def get_shape_from_transform(transform_node):
    return cmds.listRelatives(transform_node, shapes=True, fullPath=True)[0]
    x1
    
def make_unselectable(transform_node):
    shape_node = cls.get_shape_from_transform(transform_node)
    
    cls.set_attr(shape_node, "overrideEnabled", True)
    cls.set_attr(shape_node, "overrideDisplayType", 2)
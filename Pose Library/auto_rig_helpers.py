import maya.cmds as cmds

class AutoRigHelpers(object):
    
    @classmethod
    def get_attr(cls, node, attr):
        return cmds.getAttr("{0}.{1}".format(node, attr))
    
    @classmethod
    def add_attr(cls, node, long_name, attr_type, default_value, keyable=False):
        cmds.addAttr(node, longName=long_name, attributeType=attr_type, defaultValue=default_value, keyable=keyable)
        
    @classmethod
    def set_attr(cls, node, attr, value, value_type=None):
        if value_type:
            # If type is a list, unpack it for setting attributes w/ multiple values
            cmds.setAttr("{0}.{1}".format(node, attr), *value, type=value_type)
        else:
            # If attribute is being set with only one value
            cmds.setAttr("{0}.{1}".format(node, attr), value)
            
    @classmethod
    def connect_attr(cls, node_a, attr_a, node_b, attr_b, force=False):
        # Connect attribute in node a to attribute in node b
        cmds.connectAttr("{0}.{1}".format(node_a, attr_a), "{0}.{1}".format(node_b, attr_b), force=force)
        
    @classmethod
    def lock_hide_attrs(cls, node, attrs, lock=True, hide=True, channelBox=False):
        # if hide is true, the attr should NOT be keyable
        keyable = not hide
        
        # lock/hide all attrs in node
        for attr in attrs:
            full_reference = "{0}.{1}".format(node, attr)
            cmds.setAttr(full_reference, lock=lock, keyable=keyable, channelBox=channelBox)
    
    @classmethod
    def can_set_attr(cls, node, attr) -> bool:
        locked = cls.is_attr_locked(node, attr)
        connected = cls.is_attr_connected(node, attr)
        return locked == False and connected == False
        
    @classmethod
    def is_attr_connected(cls, node, attr) -> bool:
        connections = cmds.listConnections(f"{node}.{attr}", connections=True)
        
        if connections == None:
            return False
            
        for connection in connections:
            if f"{node}.{attr}" == connection and cmds.connectionInfo(connection, isDestination=True):
                return True
        return False
    
    @classmethod
    def is_attr_locked(cls, node, attr) -> bool:
        return cmds.getAttr(f"{node}.{attr}", lock=True)
    
    @classmethod
    def is_attr_keyable(cls, node, attr) -> bool:
        return cmds.getAttr(f"{node}.{attr}", keyable=True)
    
    @classmethod
    def create_display_layer(cls, name, members, reference=False):
        # Create display layer
        display_layer = cmds.createDisplayLayer(name=name, empty=True)
        
        # Set layer as reference if true
        if reference:
            cmds.setAttr("{0}.displayType".format(display_layer), 2)
            
        # Add members to layer if provided
        if members:
            cmds.editDisplayLayerMembers(display_layer, members, noRecurse=True)
            
        return display_layer
        
    @classmethod
    def create_assign_lambert_shader(cls, name, shape_node):
        # Create shader
        shader = cmds.shadingNode("lambert", name=name, asShader=True)
        shader_sg = cmds.sets(name="{0}SG".format(shader), renderable=True, noSurfaceShader=True, empty=True)
        cls.connect_attr(shader, "outColor", shader_sg, "surfaceShader")
        
        # Assign shader to shape node
        cmds.sets([shape_node], e=True, forceElement=shader_sg)
        
        return shader
    
    @classmethod
    def get_shape_from_transform(cls, transform_node):
        return cmds.listRelatives(transform_node, shapes=True, fullPath=True)[0]
        x1
        
    @classmethod
    def make_unselectable(cls, transform_node):
        shape_node = cls.get_shape_from_transform(transform_node)
        
        cls.set_attr(shape_node, "overrideEnabled", True)
        cls.set_attr(shape_node, "overrideDisplayType", 2)
        
    @classmethod
    def uuid_to_name(cls, uuid) -> str:
        return cmds.ls(uuid, shortNames=True)[0]
    
    @classmethod
    def uuid_to_full_path(cls, uuid) -> str:
        return cmds.ls(uuid, long=True)[0]
        
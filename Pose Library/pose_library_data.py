import maya.cmds as cmds

from auto_rig_helpers import AutoRigHelpers

class PoseData(object):
    
    # Constructor that initializes the pose's data
    #
    # @param control_nodes - Contains a list of all the control nodes and its data
    #
    def __init__(self, control_nodes=None):
        self.control_nodes = []
        # If no control nodes were given, return
        if control_nodes == None:
            return
            
        for control_node in range(len(control_nodes)):
            self.add_control_node(ControlNodeData(control_nodes[control_node]))
            
    def add_control_node(self, control_node):
        self.control_nodes.append(control_node)
        
class ControlNodeData(object):
    
    # Constructor that is used to initialize the control node's data
    #
    # @param control_node_uuid - The control node's UUID
    def __init__(self, control_node_uuid=None):
        self.attributes = {}
        
        # If no control node was given, return
        if control_node_uuid == None:
            return
        
        self.uuid = control_node_uuid
        self.name = AutoRigHelpers.uuid_to_name(self.uuid)
        self.full_path = AutoRigHelpers.uuid_to_full_path(self.uuid)
        
        self.attributes["translate"] = AutoRigHelpers.get_attr(self.full_path, "translate")[0]
        self.attributes["rotate"] = AutoRigHelpers.get_attr(self.full_path, "rotate")[0]
        self.attributes["scale"] = AutoRigHelpers.get_attr(self.full_path, "scale")[0]
    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value
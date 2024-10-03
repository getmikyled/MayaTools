import maya.cmds as cmds
import ast

from pose_library_io_utility import PoseLibraryIOUtility

from pose_library_data import PoseData
from pose_library_data import ControlNodeData

from auto_rig_helpers import AutoRigHelpers

class PoseLibrary(object):
    
    selected_folder = ""
    poses = {}
    
    @classmethod
    def update_selected_folder(cls, new_folder):
        cls.selected_folder = new_folder
        
        folder_path = PoseLibraryIOUtility.folders[new_folder]
        cls.poses = PoseLibraryIOUtility.get_poses_at_path(folder_path)
        
    @classmethod
    def load_pose_to_rig(cls, pose_data):
        # Iterate through every control node
        for n in range(len(pose_data.control_nodes)):
            # Get the control node's data and full path
            control_node_data = pose_data.control_nodes[n]
            control_node = control_node_data.full_path
            
            # Iterate through attributes and set data
            for attr, value in control_node_data.attributes.items():
                # Convert string into tuple
                values = ast.literal_eval(value)
                
                try:
                    # Check if the x, y, and z values for each attribute are settable individually
                    if AutoRigHelpers.can_set_attr(control_node, f"{attr}X"):
                        AutoRigHelpers.set_attr(control_node, f"{attr}X", values[0])
                    if AutoRigHelpers.can_set_attr(control_node, f"{attr}Y"):
                        AutoRigHelpers.set_attr(control_node, f"{attr}Y", values[1])
                    if AutoRigHelpers.can_set_attr(control_node, f"{attr}Z"):
                        AutoRigHelpers.set_attr(control_node, f"{attr}Z", values[2])
                except:
                    pass
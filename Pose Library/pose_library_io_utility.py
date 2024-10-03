import sys
import os

import maya.cmds as cmds

from pose_library_data import PoseData
from pose_library_data import ControlNodeData

class PoseLibraryIOUtility(object):

    CN_START = 1
    CN_ATTR_START = 5
    CN_ATTR_COUNT = 3
    CN_ATTR_INC = 7

    RIG_CAPTURE_WIDTH = 500
    RIG_CAPTURE_HEIGHT = 400

    root_folder_path = ""
    folders = {}
    
    @classmethod
    def create_static_folders(cls):
        # Get root folder path
        workspace_path = cmds.workspace(query=True, rootDirectory=True)
        cls.root_folder_path = os.path.join(workspace_path, "PoseLibrary")
        
        # Create "PoseLibrary" folder
        cls.create_folder(cls.root_folder_path)
        
    @classmethod
    def create_folder(cls, folder_path, exists_ok=True):
        os.makedirs(folder_path, exist_ok=exists_ok)    
        
    @classmethod
    def save_pose_data(cls, pose_data : PoseData, save_path, pose_name):
        pose_file_path = os.path.join(save_path, f"{pose_name}.pose")
        
        with open(pose_file_path, 'w') as pose_file:
            # Write pose name to file
            cls.write_line_to_file(pose_file, "pose_name", pose_name)
            
            # Iterate through all the control nodes
            for control_node in pose_data.control_nodes:
                pose_file.write("\n")
                
                # Write node references
                cls.write_line_to_file(pose_file, "uuid", control_node.uuid)
                cls.write_line_to_file(pose_file, "name", control_node.name)
                cls.write_line_to_file(pose_file, "full_path", control_node.full_path)
                
                # Write node attributes
                for attribute, value in control_node.attributes.items():
                    cls.write_line_to_file(pose_file, attribute, value)
            
    @classmethod
    def load_pose_data(cls, pose_path):
        # Create Pose Data
        pose_data = PoseData()
        
        # Read lines in PoseData
        with open(pose_path, 'r') as pose_file:
            lines = pose_file.readlines()
            
        # Read poses name
        pose_name = cls.read_value_from_property(lines[0])
        
        # Iterate through all control nodes
        for n in range(cls.CN_START, len(lines), cls.CN_ATTR_INC):
            # Create Control Node Data
            control_node_data = ControlNodeData()
            pose_data.add_control_node(control_node_data)
            
            # Read control node properties
            control_node_data.uuid = cls.read_value_from_property(lines[n+1])
            control_node_data.name = cls.read_value_from_property(lines[n+2])
            control_node_data.full_path = cls.read_value_from_property(lines[n+3])
            
            # Read control node attributes
            for attr_num in range(cls.CN_ATTR_COUNT):
                line = lines[cls.CN_ATTR_START+attr_num]
                control_node_data.add_attribute(cls.read_property(line), cls.read_value_from_property(line))
        
        return pose_data
            
    @classmethod
    def read_value_from_property(cls, line):
        return line.split(": ")[1].strip()
        
    @classmethod
    def read_property(cls, line):
        return line.split(": ")[0]
    
    @classmethod
    def write_line_to_file(cls, file, property, value):
        file.write(f"{property}: {value}\n")
    
    @classmethod
    def get_poses_at_path(cls, folder_path):
        poses = {}
        
        # Get items at folder path
        items = os.listdir(folder_path)
        
        for item in items:
            # Get pose path
            pose_path = os.path.join(folder_path, item)
            
            # Check if item is a ".pose" file
            if os.path.isfile(pose_path) and item.endswith(".pose"):
                pose_data = cls.load_pose_data(pose_path)
                poses[item.split(".pose")[0]] = pose_data
        return poses
        
    @classmethod
    def load_folders_to_hierarchy(cls, pose_library_window, hierarchy_parent, root_path, reset_folders):
        if reset_folders:
            cls.folders = {}
            cls.folders[os.path.basename(root_path)] = root_path
        
        items = os.listdir(root_path)
        
        for item in items:
            # Check if item is a directory
            folder_path = os.path.join(root_path, item)
            if os.path.isdir(folder_path):
                # Save folder name and folder path to dictionary
                cls.folders[item] = folder_path
                
                folder_hierarchy_item = pose_library_window.create_hierarchy_item(item)
                pose_library_window.add_to_hierarchy(hierarchy_parent, folder_hierarchy_item)
                
                # Recursively call function on this folder
                cls.load_folders_to_hierarchy(pose_library_window, folder_hierarchy_item, folder_path, False)
        
    @classmethod
    def capture_rig_image(cls, rig_capture_path, capture_width=RIG_CAPTURE_HEIGHT, capture_height=RIG_CAPTURE_HEIGHT):
        # Capture image of rig
        cmds.playblast(
            completeFilename=rig_capture_path,
            format='image',
            viewer=False,
            framePadding=4,
            width=capture_width,
            height=capture_height,
            percent=100,
            quality=100,
            showOrnaments=False,
            startTime=cmds.currentTime(query=True),
            endTime=cmds.currentTime(query=True)
        )
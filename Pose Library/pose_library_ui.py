import sys
import os

from functools import partial

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from shiboken6 import wrapInstance

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from pose_library import PoseLibrary
from pose_library_io_utility import PoseLibraryIOUtility
from pose_library_data import PoseData

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    
    # Account for system versions
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class NewFolderDialog(QtWidgets.QDialog):
    
    X_SIZE = 300
    Y_SIZE = 115
    
    def __init__(self, pose_library_window, parent=maya_main_window()):
        super(NewFolderDialog, self).__init__(parent)
        
        # Cache pose library window
        self.pose_library_window = pose_library_window
        
        # Set window proprties
        self.setWindowTitle("New Folder")
        self.setMinimumSize(self.X_SIZE, self.Y_SIZE)
        self.setMaximumSize(self.X_SIZE, self.Y_SIZE)
        
        # Prevent 'x'/ close button from being pressed
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~QtCore.Qt.WindowCloseButtonHint)
        
        # Create widgets and layouts
        self.create_widgets()
        self.create_layouts()
        
    def create_widgets(self):
        # Folder name widgets
        self.folder_name_label = QtWidgets.QLabel("Folder Name")
        self.folder_name_line_edit = QtWidgets.QLineEdit("New Folder")
        
        # Button widgets
        self.confirm_btn = QtWidgets.QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self.create_new_folder)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addWidget(self.folder_name_label)
        main_layout.addWidget(self.folder_name_line_edit)
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.stretch(True)
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(btn_layout)
        
    def create_new_folder(self):
        new_folder_name = self.folder_name_line_edit.text()
        folder_path = os.path.join(PoseLibraryIOUtility.root_folder_path, new_folder_name)
        PoseLibraryIOUtility.create_folder(folder_path)
        self.pose_library_window.refresh_hierarchy()
        
        self.close()
        
class SavePoseDialog(QtWidgets.QDialog):
    
    X_SIZE = 300
    Y_SIZE = 175
    
    def __init__(self, pose_library_window, parent=maya_main_window()):
        super(SavePoseDialog, self).__init__(parent)
        
        # Cache Pose Library
        self.pose_library_window = pose_library_window
        
        # Set window properties
        self.setWindowTitle("Save Pose")
        self.setMinimumSize(self.X_SIZE, self.Y_SIZE)
        self.setMaximumSize(self.X_SIZE, self.Y_SIZE)
        
        # Prevent 'x'/ close button from being pressed
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~QtCore.Qt.WindowCloseButtonHint)
        
        # Create widgets and layouts
        self.create_widgets()
        self.create_layouts()
        
        # Inital Capture Rig Image
        self.take_rig_capture()

    def create_widgets(self):
        # Folder name widgets
        self.pose_name_label = QtWidgets.QLabel("Pose Name")
        self.pose_name_line_edit = QtWidgets.QLineEdit("New Pose")
        
        self.rig_capture_btn = QtWidgets.QPushButton("Take Rig Capture")
        self.rig_capture_btn.clicked.connect(self.take_rig_capture)
        
        # Button widgets
        self.confirm_btn = QtWidgets.QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self.save_pose)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addWidget(self.pose_name_label)
        main_layout.addWidget(self.pose_name_line_edit)
        
        rig_capture_layout = QtWidgets.QVBoxLayout()
        rig_capture_layout.addWidget(self.rig_capture_btn)
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.stretch(True)
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(rig_capture_layout)
        main_layout.addLayout(btn_layout)
        
    def save_pose(self):
        # Tell the PoseLibrary to save the pose
        pose_name = self.pose_name_line_edit.text()
        self.pose_library_window.save_pose(pose_name)
        
        self.close()
        
    def take_rig_capture(self):
        rig_capture_dir_path = self.pose_library_window.get_save_folder_path()
        rig_capture_name = self.pose_name_line_edit.text()
        rig_capture = os.path.join(rig_capture_dir_path, rig_capture_name + ".png")
        PoseLibraryIOUtility.capture_rig_image(rig_capture)
        
class PoseLibraryWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    
    HIERARCHY_WIDGET_WIDTH = 225
    CONTENT_WIDGET_WIDTH = 400
    
    RIG_CAPTURE_SCALAR = 0.5
    
    @property
    def CONTENT_BUTTON_WIDTH(self):
        return PoseLibraryIOUtility.RIG_CAPTURE_WIDTH * self.RIG_CAPTURE_SCALAR
        
    @property
    def CONTENT_BUTTON_HEIGHT(self):
        return PoseLibraryIOUtility.RIG_CAPTURE_HEIGHT * self.RIG_CAPTURE_SCALAR
    
    def __init__(self, parent=maya_main_window()):
        super(PoseLibraryWindow, self).__init__(parent)
        
        PoseLibraryIOUtility.create_static_folders()
        
        self.setWindowTitle("Pose Library")
        self.setMinimumSize(self.HIERARCHY_WIDGET_WIDTH + self.CONTENT_WIDGET_WIDTH, 700)
        
        # Create widgets and layouts
        self.create_widgets()
        self.create_layouts()
        
        self.refresh_hierarchy()
        
    def create_widgets(self):
        self.create_toolbar()
        self.create_hierarchy_widgets()
        self.create_content_widgets()
        
    def create_toolbar(self):
        # Create the toolbar
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.toggleViewAction().setEnabled(False)
        
        # Create 'New Folder' action
        self.new_folder_action = QtGui.QAction(QtGui.QIcon(), "New Folder", self)
        self.new_folder_action.triggered.connect(self.open_new_folder_dialog)
        
        # Create 'Save Pose' action
        self.save_pose_action = QtGui.QAction(QtGui.QIcon(), "Save Pose", self)
        self.save_pose_action.triggered.connect(self.open_save_pose_dialog)
        
        # Add actions
        self.toolbar.addAction(self.new_folder_action)
        self.toolbar.addAction(self.save_pose_action)   
        
    # Create Tree Hierarchy Widgets
    def create_hierarchy_widgets(self):
        self.hierarchy_area = QtWidgets.QWidget()
        
        # Create Hierarchy TreeView & StandardItemModel
        self.hierarchy_tree = QtWidgets.QTreeView()
        self.hierarchy_model = QtGui.QStandardItemModel()
        self.hierarchy_model.setHorizontalHeaderLabels(["Workspace/PoseLibrary"])
        self.hierarchy_tree.setModel(self.hierarchy_model)
        
        self.hierarchy_tree.selectionModel().selectionChanged.connect(self.update_selected_folder)
        
    def create_content_widgets(self):
        self.content_widget = QtWidgets.QWidget()
        
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidget(self.content_widget)
        self.content_area.setWidgetResizable(True)    
        
    def create_layouts(self):
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(splitter)
        
        # Create Hierarchy Area for Splitter - Contains the Folder Hierarchy
        hierarchy_layout = QtWidgets.QVBoxLayout()
        self.hierarchy_area.setLayout(hierarchy_layout)
        
        hierarchy_layout.addWidget(self.hierarchy_tree)        
        
        # Create the Content Area for Splitter - Contains Folder Content
        self.content_layout = QtWidgets.QGridLayout()
        self.content_widget.setLayout(self.content_layout)
        
        splitter.addWidget(self.hierarchy_area)
        splitter.addWidget(self.content_area)
        splitter.setSizes([self.HIERARCHY_WIDGET_WIDTH, self.CONTENT_WIDGET_WIDTH])
    
    def open_new_folder_dialog(self):
        try:
            self.new_folder_dialog.close()
            self.new_folder_dialog.deleteLater()
        except:
            pass
            
        self.new_folder_dialog = NewFolderDialog(self)
        self.new_folder_dialog.show()
        
    def open_save_pose_dialog(self):
        try:
            self.save_pose_dialog.close()
            self.save_pose_dialog.deleteLater()
        except:
            pass
            
        self.save_pose_dialog = SavePoseDialog(self)
        self.save_pose_dialog.show()
    
    def add_to_hierarchy(self, hierarchy_parent, hierarchy_item):
        hierarchy_parent.appendRow(hierarchy_item)
        
    def create_hierarchy_item(self, text, editable=False):
        # Create Hierarchy Item
        hierarchy_item = QtGui.QStandardItem(text)
        hierarchy_item.setEditable(editable)
        
        return hierarchy_item
        
    def update_selected_folder(self, selected, deselected):
        # Get the data of the first selected item
        selected_indexes = selected.indexes()
        if selected_indexes:
            selected_item = selected_indexes[0].data()
            
            # Update the PoseLibrary's selected_folder
            PoseLibrary.update_selected_folder(selected_item)
            
        # Update the content UI
        self.refresh_content_layout()
        
    def refresh_hierarchy(self):
        self.hierarchy_model.clear()
        self.hierarchy_model.setHorizontalHeaderLabels(["Workspace/PoseLibrary"])
        
        # Add root folder to hierarchy
        self.hierarchy_root = self.create_hierarchy_item("PoseLibrary")
        self.add_to_hierarchy(self.hierarchy_model, self.hierarchy_root)
        
        PoseLibraryIOUtility.load_folders_to_hierarchy(self, self.hierarchy_root, PoseLibraryIOUtility.root_folder_path, True)
        
        selection_model = self.hierarchy_tree.selectionModel()
        index = self.hierarchy_model.indexFromItem(self.hierarchy_model.invisibleRootItem().child(0))
        selection_model.select(index, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        
        
    def refresh_content_layout(self):
        # Clear Content Layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item is not None:
                item.widget().deleteLater()
            item = None
        
        for i in range(5):
            self.content_layout.setRowStretch(i, 1)  # Equal stretch for all rows
            self.content_layout.setColumnStretch(i, 1)  # Equal stretch for all columns
        
        # Add new poses to content layout
        for pose_name, pose_data in PoseLibrary.poses.items():
            self.create_content_button(pose_name, pose_data)
        
        
    # Create the buttons that load rig poses in the pose library content window
    def create_content_button(self, pose_name="", pose_data=PoseData()):
        
        # Create button container and layout
        button_container = QtWidgets.QWidget()
        button_container.setFixedSize(self.CONTENT_BUTTON_WIDTH + 50, self.CONTENT_BUTTON_HEIGHT + 50)
        button_layout = QtWidgets.QVBoxLayout()
        button_container.setLayout(button_layout)
        
        # Create button
        button = QtWidgets.QPushButton()
        button.setFixedSize(self.CONTENT_BUTTON_WIDTH, self.CONTENT_BUTTON_HEIGHT)
        
        # Connect loading the rig pose to the button
        button.clicked.connect(partial(PoseLibrary.load_pose_to_rig, pose_data))
        
        # Add rig capture to button
        selected_folder = PoseLibraryIOUtility.folders[PoseLibrary.selected_folder]
        pose_capture = os.path.join(selected_folder, pose_name + ".png")
        if os.path.exists(pose_capture):
            pose_icon = QtGui.QIcon(pose_capture)
            button.setIcon(pose_icon)
            button.setIconSize(button.size())
            
        # Create Label
        button_label = QtWidgets.QLabel(pose_name)
        
        # Add widgets to button layout
        button_layout.addWidget(button)
        button_layout.addWidget(button_label)
        
        # Add button to content_layout
        self.content_layout.addWidget(button_container)
        
    # Is called when the "Save Pose" button in the tool bar is pressed
    def save_pose(self, pose_name):
        selection = cmds.ls(selection=True, uuid=True)
        pose_path = self.get_save_folder_path()
        PoseLibraryIOUtility.save_pose_data(PoseData(selection), pose_path, pose_name)
        
        # Refresh the selected folder's contents
        PoseLibrary.update_selected_folder(PoseLibrary.selected_folder)
        self.refresh_content_layout()
        
    def get_save_folder_path(self) -> str:
        return PoseLibraryIOUtility.folders[PoseLibrary.selected_folder]
        
if __name__ == "__main__":
    try:
        pose_library_ui.close()
        pose_library_ui.deleteLater()
    except:
        pass
        
    pose_library_ui = PoseLibraryWindow()
    pose_library_ui.show(dockable=True)
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from ball_auto_rig import BallAutoRig

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    
    # Account for system versions
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
        
class BallAutoRigDialog(QtWidgets.QDialog):

    primary_color = "#7AD8D0"
    secondary_color = "#F5C82E"

    def __init__(self, parent=maya_main_window()):
        super(BallAutoRigDialog, self).__init__(parent)
        
        self.setWindowTitle("Ball Auto Rigger")
        self.setMinimumSize(300, 200)
        self.setMaximumSize(300, 200)
        
        self.__create_widgets()
        self.__create_layouts()
        self.__create_connections()
        
    def __create_widgets(self):
        self.primary_color_text = QtWidgets.QLabel("Primary")
        self.primary_color_btn = QtWidgets.QPushButton()
        self.primary_color_btn.setStyleSheet("background-color: {0}".format(self.primary_color))
        self.primary_color_dialog = QtWidgets.QColorDialog()
        self.secondary_color_text = QtWidgets.QLabel("Secondary")
        self.secondary_color_btn = QtWidgets.QPushButton()
        self.secondary_color_btn.setStyleSheet("background-color: {0}".format(self.secondary_color))
        self.secondary_color_dialog = QtWidgets.QColorDialog()
        self.create_ball_rig_btn = QtWidgets.QPushButton("Create Ball Rig")
        
    def __create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        colors_layout = QtWidgets.QVBoxLayout()
        primary_color_layout = QtWidgets.QHBoxLayout()
        primary_color_layout.addWidget(self.primary_color_text)
        primary_color_layout.addWidget(self.primary_color_btn)
        secondary_color_layout = QtWidgets.QHBoxLayout()
        secondary_color_layout.addWidget(self.secondary_color_text)
        secondary_color_layout.addWidget(self.secondary_color_btn)
        colors_layout.addLayout(primary_color_layout)
        colors_layout.addLayout(secondary_color_layout)
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 25, 0, 0)
        btn_layout.addWidget(self.create_ball_rig_btn)
        
        main_layout.addLayout(colors_layout)
        main_layout.addLayout(btn_layout)
        
    def __create_connections(self):
        self.primary_color_btn.clicked.connect(self.__update_primary_color)
        self.secondary_color_btn.clicked.connect(self.__update_secondary_color)
        
        self.primary_color_dialog.currentColorChanged.connect(self.__update_primary_color)
        self.secondary_color_dialog.currentColorChanged.connect(self.__update_secondary_color)
        
        self.create_ball_rig_btn.clicked.connect(self.__create_ball_rig)
        
    def __update_primary_color(self):
        self.primary_color = self.primary_color_dialog.getColor().name()
        self.primary_color_btn.setStyleSheet("background-color: {0}".format(self.primary_color))
        
    def __update_secondary_color(self):
        self.secondary_color = self.secondary_color_dialog.getColor().name()
        self.secondary_color_btn.setStyleSheet("background-color: {0}".format(self.secondary_color))
        
    def __create_ball_rig(self):
        ball_rig = BallAutoRig()
        #ball_rig.set_colors(self.__hex_to_rgb(self.primary_color), self.__hex_to_rgb(self.secondary_color))
        ball_rig.construct_rig()
        
    def __hex_to_rgb(self, hex_code):
        # Strip leading # if present
        hex_code = hex_code.lstrip('#')
        
        # Extract rgb from hex code
        rgb = tuple(int(hex_code[i:i+2], 16) / 256 for i in (0, 2, 4))
        return rgb
       
        
if __name__ == "__main__":
    
    try:
        ball_auto_rig_dialog.close()
        ball_auto_rig_dialog.deleteLater()
    except:
        pass
    
    ball_auto_rig_dialog = BallAutoRigDialog()
    ball_auto_rig_dialog.show()
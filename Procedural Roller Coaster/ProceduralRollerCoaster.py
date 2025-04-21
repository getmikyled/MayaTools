import maya.cmds as cmds
from ProceduralHelpers import ProceduralHelpers as ph

class ProceduralRollerCoaster(object):
    
    left_track_geo = "LeftTrack_GEO"
    right_track_geo = "RightTrack_GEO"
    
    def __init__(self, input_curve):
        self.input_curve = input_curve
        self.__sweep_track()
        
    def __sweep_track(self):
        sweep_geo = cmds.sweepMeshFromCurve(self.input_curve)
        sweep_geo = ph.rename(sweep_geo, "ProceduralTrack_GEO")
        
        
        
rct = ProceduralRollerCoaster(cmds.ls(sl=True))

def unfold_uvs(objects):
    for object in objects:
        cmds.unfold(object, 
                    globalBlend=1.0,   # Full unfold effect
                    iterations=1,      # More iterations for smoothness
                    pinSelected=False, # Allow all UVs to relax
                    optimizeAxis=0)  # Tries to keep UVs aligned

def select_metal_faces(objects):
    obj = objects[1]
    all_metal_faces = []
    for start in range(1,6):
        total_faces = cmds.polyEvaluate(obj, face=True)
        metal_faces = [f"{obj}.f[{i}]" for i in range (start,total_faces,14)]
        all_metal_faces.join(metal_faces)
        
    cmds.select(all_metal_faces)

objs = cmds.ls(selection=True, flatten=True)
select_metal_faces(objs)

unfold_uvs(selected_objects = cmds.ls(selection=True, flatten=True))

obj = cmds.ls(selection=True, flatten=True)[0]
total_faces = cmds.polyEvaluate(obj, face=True)
metal_faces = [f"{obj}.f[{i}]" for i in range (0,total_faces,14)]
cmds.select(metal_faces)
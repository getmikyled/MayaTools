import maya.cmds as cmds

class ProceduralHelpers(object):
    
    @classmethod
    def rename(cls, old_name, new_name) -> str:
        cmds.rename(old_name, new_name)
        return new_name
import maya.cmds as cmds

def circle(name='circle_CTRL', size=1):
    circle = cmds.circle(n=name, r=size, nrx=1, nry=0, nrz=0)
    return circle
        
    
def cube(name='cube_CTRL', size = 1):
    # Create Cube
    cube = cmds.curve(n=name, d=1, p=[(-1,-1,-1), (-1,-1,1), (-1,1,1), (-1,1,-1), 
         (-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (1,1,-1), (1,1,1), (1,-1,1),
         (1,-1,-1), (1,-1,1), (-1,-1,1), (-1,1,1), (1,1,1)])
         
    # Scale cube
    cmds.scale( size, size, size, cube, pivot=(1, 0, 0), absolute=True)
    
    return cube
    
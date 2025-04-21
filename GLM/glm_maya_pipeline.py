import maya.cmds as cmds
import os
import re

def get_folder_parent(file_path, count=1):
    current_path = file_path
    for i in range(count):
        current_path = os.path.dirname(current_path)
    return current_path
    
def get_animation_range():
    ''' Returns the animation range in list form as [Start, End].'''
    animation_range = []
    animation_range.append(cmds.playbackOptions(query=True, ast=True))
    animation_range.append(cmds.playbackOptions(query=True, aet=True))
    return animation_range
    
print(get_animation_range())

def export_all_as_usd(exportPath):
    #file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=0;staticSingleSample=0;startTime=0;endTime=20;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;rootPrim=;rootPrimType=scope;defaultPrim=pCube1;exportMaterials=1;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportAssignedMaterials=1;exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;includeEmptyTransforms=1;stripNamespaces=0;worldspace=0;exportStagesAsRefs=1;excludeExportTypes=[];legacyMaterialScope=0" -type "USD Export" -pr -ea "E:/GameAssets/bruh.usd";
    cmds.file(exportPath
              force=True, 
              options=';exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=0;staticSingleSample=0;startTime=0;endTime=20;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;rootPrim=;rootPrimType=scope;defaultPrim=pCube1;exportMaterials=1;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportAssignedMaterials=1;exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;includeEmptyTransforms=1;stripNamespaces=0;worldspace=0;exportStagesAsRefs=1;excludeExportTypes=[];legacyMaterialScope=0',
              type='USD Export',
              preserveReferences=True,
              exportAll=True)

filePath = cmds.file(query=True, sceneName=True)

def find_obj_with_string_in_name(str):
    objs =  cmds.ls()
    for obj in objs:
        if str in obj:
            return obj
            
    raise Exception(f'Error: Failed to find obj with "{str}" in it')
            

def select_deforming_geometry():
    # Find the root object of the geometry, characterized by 'modelMain'
    try:
        root = find_obj_with_string_in_name('modelMain')
    except Exception as e:
        print(e)
        return False

    # Get set of deforming geometry
    deforming_geo = set()
    descendents = cmds.listRelatives(root, allDescendents=True, fullPath=True) or []
    for descendent in descendents:
        # Check if node is of type 'mesh'
        if cmds.nodeType(descendent) == 'mesh':
            parent = cmds.listRelatives(descendent, parent=True, fullPath=True)
            if parent[0] not in deforming_geo:
                deforming_geo.add(parent[0])
                
    cmds.select(list(deforming_geo))
    return True
    
select_deforming_geometry()



# Get file name
baseFileName = os.path.splitext(os.path.basename(filePath))[0]
animCacheFileName = fileName.replace('base', 'animcache')
toUsdFileName = file_name.replace('base', 'toUSD'

modelName = 'GAMMA'
version = re.search(r'[0-9]{4}', file_name).group()
cacheName = f'{model_name.lower().title()}{version}'
print(cacheName)

print(filePath)
bakePath = os.path.join(get_folder_parent(filePath, 4), f'_ASSETS/CACHE/{modelName}/GEOCACHE')
print(bakePath)
cacheFormat ='mcx'

# Note: If it doesn't work, might need to add ia key arg,
# cacheFile -attachFile -fileName "CACHEEEE" -directory "E:/GameAssets/MEH Game Jam/character/Cache/"  -cacheFormat "mcx"  -ia cacheSwitch1.inp[0];
cmds.cacheFile(attachFile=True, fileName=cacheName, directory=bakePath, cacheFormat=cacheFormat)
            
# Chair FBX Generator Script (placeholder)
# Fill in the code to generate a chair model in Blender and export as FBX.

import bpy
import os

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_chair():
    # TODO: Add code to generate chair geometry
    pass

def export_fbx(filepath):
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=False)

if __name__ == "__main__":
    clear_scene()
    create_chair()
    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "chair.fbx"
    )
    export_fbx(export_path)
    print(f"Exported chair to {export_path}")

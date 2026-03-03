import bpy
import os

# Delete all existing objects
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Create a simple bookshelf
def create_bookshelf():
    # Dimensions
    width = 2.0
    height = 2.5
    depth = 0.3
    shelf_thickness = 0.05
    num_shelves = 4

    # Create the sides
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-width/2 + shelf_thickness/2, 0, height/2))
    left = bpy.context.active_object
    left.scale = (shelf_thickness/2, depth/2, height/2)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2 - shelf_thickness/2, 0, height/2))
    right = bpy.context.active_object
    right.scale = (shelf_thickness/2, depth/2, height/2)

    # Create the top
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height - shelf_thickness/2))
    top = bpy.context.active_object
    top.scale = (width/2, depth/2, shelf_thickness/2)

    # Create the bottom
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, shelf_thickness/2))
    bottom = bpy.context.active_object
    bottom.scale = (width/2, depth/2, shelf_thickness/2)

    # Create the shelves
    for i in range(1, num_shelves+1):
        z = i * (height - shelf_thickness) / (num_shelves + 1)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z + shelf_thickness/2))
        shelf = bpy.context.active_object
        shelf.scale = (width/2 - shelf_thickness, depth/2 - 0.01, shelf_thickness/2)

# Export as FBX
def export_fbx(filepath):
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=False)

if __name__ == "__main__":
    clear_scene()
    create_bookshelf()
    # Set export path to the current Blender file directory or desktop
    export_path = os.path.join(os.path.expanduser("~"), "Desktop", "bookshelf.fbx")
    export_fbx(export_path)
    print(f"Exported bookshelf to {export_path}")

import bpy
import bmesh
import os


# -------------------------
# CONFIG
# -------------------------
WIDTH = 2.4
HEIGHT = 2.2
DEPTH = 0.6

FRAME_THICKNESS = 0.15
HEARTH_HEIGHT = 0.2
MANTEL_HEIGHT = 1.6
MANTEL_DEPTH = 0.25


# -------------------------
# UTIL
# -------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def add_box(bm, x_min, x_max, y_min, y_max, z_min, z_max):
    v = [
        bm.verts.new((x_min, y_min, z_min)),
        bm.verts.new((x_max, y_min, z_min)),
        bm.verts.new((x_max, y_max, z_min)),
        bm.verts.new((x_min, y_max, z_min)),

        bm.verts.new((x_min, y_min, z_max)),
        bm.verts.new((x_max, y_min, z_max)),
        bm.verts.new((x_max, y_max, z_max)),
        bm.verts.new((x_min, y_max, z_max)),
    ]

    faces = [
        (0,1,2,3),
        (4,5,6,7),
        (0,1,5,4),
        (1,2,6,5),
        (2,3,7,6),
        (3,0,4,7)
    ]

    for f in faces:
        try:
            bm.faces.new([v[i] for i in f])
        except:
            pass


# -------------------------
# FIREPLACE
# -------------------------
def create_fireplace():

    mesh = bpy.data.meshes.new("FireplaceMesh")
    obj = bpy.data.objects.new("Fireplace", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    half_w = WIDTH / 2
    half_d = DEPTH / 2

    # -------------------------
    # Outer Frame
    # -------------------------
    add_box(
        bm,
        -half_w,
        half_w,
        -half_d,
        half_d,
        0,
        HEIGHT
    )

    # -------------------------
    # Firebox cavity (front opening)
    # Instead of boolean, build internal void walls
    # -------------------------

    cavity_width = WIDTH - 2 * FRAME_THICKNESS
    cavity_height = HEIGHT - FRAME_THICKNESS
    cavity_depth = DEPTH - FRAME_THICKNESS

    c_half_w = cavity_width / 2
    c_half_d = cavity_depth / 2

    # Remove front center by adding inner "negative space" walls
    # Left inner wall
    add_box(
        bm,
        -c_half_w,
        -c_half_w + FRAME_THICKNESS,
        -c_half_d,
        c_half_d,
        HEARTH_HEIGHT,
        cavity_height
    )

    # Right inner wall
    add_box(
        bm,
        c_half_w - FRAME_THICKNESS,
        c_half_w,
        -c_half_d,
        c_half_d,
        HEARTH_HEIGHT,
        cavity_height
    )

    # Top inner wall
    add_box(
        bm,
        -c_half_w,
        c_half_w,
        -c_half_d,
        c_half_d,
        cavity_height - FRAME_THICKNESS,
        cavity_height
    )

    # Back panel
    add_box(
        bm,
        -c_half_w,
        c_half_w,
        c_half_d - FRAME_THICKNESS,
        c_half_d,
        HEARTH_HEIGHT,
        cavity_height
    )

    # -------------------------
    # Hearth Slab
    # -------------------------
    add_box(
        bm,
        -half_w * 0.8,
        half_w * 0.8,
        -half_d - 0.1,
        half_d,
        0,
        HEARTH_HEIGHT
    )

    # -------------------------
    # Mantel Shelf
    # -------------------------
    add_box(
        bm,
        -half_w * 0.9,
        half_w * 0.9,
        -half_d - MANTEL_DEPTH,
        -half_d + FRAME_THICKNESS,
        MANTEL_HEIGHT,
        MANTEL_HEIGHT + FRAME_THICKNESS
    )

    # Finalize
    bm.to_mesh(mesh)
    bm.free()

    return obj


# -------------------------
# EXPORT
# -------------------------
def export_fbx(filepath):
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=False)


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    clear_scene()
    create_fireplace()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "fireplace.fbx"
    )

    export_fbx(export_path)

    print("Fireplace exported.")
import bpy
import bmesh
import os

# -------------------------
# CONFIG
# -------------------------
WIDTH = 2.4
HEIGHT = 2.2
DEPTH = 0.6

FRAME = 0.2
OPENING_HEIGHT = 1.2


# -------------------------
# UTIL
# -------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def add_box(bm, xmin, xmax, ymin, ymax, zmin, zmax):
    v = [
        bm.verts.new((xmin, ymin, zmin)),
        bm.verts.new((xmax, ymin, zmin)),
        bm.verts.new((xmax, ymax, zmin)),
        bm.verts.new((xmin, ymax, zmin)),
        bm.verts.new((xmin, ymin, zmax)),
        bm.verts.new((xmax, ymin, zmax)),
        bm.verts.new((xmax, ymax, zmax)),
        bm.verts.new((xmin, ymax, zmax)),
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

    opening_w = WIDTH - 2 * FRAME

    # -------------------------
    # LEFT WALL
    # -------------------------
    add_box(
        bm,
        -half_w,
        -half_w + FRAME,
        -half_d,
        half_d,
        0,
        HEIGHT
    )

    # -------------------------
    # RIGHT WALL
    # -------------------------
    add_box(
        bm,
        half_w - FRAME,
        half_w,
        -half_d,
        half_d,
        0,
        HEIGHT
    )

    # -------------------------
    # TOP BEAM
    # -------------------------
    add_box(
        bm,
        -half_w,
        half_w,
        -half_d,
        half_d,
        OPENING_HEIGHT,
        OPENING_HEIGHT + FRAME
    )

    # -------------------------
    # BACK WALL (inside cavity)
    # -------------------------
    add_box(
        bm,
        -opening_w/2,
        opening_w/2,
        half_d - FRAME,
        half_d,
        0,
        OPENING_HEIGHT
    )

    # -------------------------
    # HEARTH
    # -------------------------
    add_box(
        bm,
        -half_w * 0.8,
        half_w * 0.8,
        -half_d - 0.2,
        half_d,
        0,
        FRAME
    )

    bm.to_mesh(mesh)
    bm.free()

    return obj


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

    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=False)

    print("Fireplace exported.")
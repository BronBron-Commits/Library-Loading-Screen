import bpy
import bmesh
import os

# -------------------------
# CONFIG
# -------------------------
SEAT_WIDTH = 0.6
SEAT_DEPTH = 0.6
SEAT_THICKNESS = 0.06
SEAT_HEIGHT = 0.5

LEG_THICKNESS = 0.06

BACK_HEIGHT = 0.7
BACK_THICKNESS = 0.05

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
# CHAIR
# -------------------------
def create_chair():

    mesh = bpy.data.meshes.new("ChairMesh")
    obj = bpy.data.objects.new("Chair", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    half_w = SEAT_WIDTH / 2
    half_d = SEAT_DEPTH / 2

    # -------------------------
    # SEAT
    # -------------------------
    add_box(
        bm,
        -half_w,
        half_w,
        -half_d,
        half_d,
        SEAT_HEIGHT,
        SEAT_HEIGHT + SEAT_THICKNESS
    )

    # -------------------------
    # LEGS
    # -------------------------
    leg_offset_x = half_w - LEG_THICKNESS
    leg_offset_y = half_d - LEG_THICKNESS

    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(
                bm,
                sx * leg_offset_x,
                sx * leg_offset_x + LEG_THICKNESS * sx,
                sy * leg_offset_y,
                sy * leg_offset_y + LEG_THICKNESS * sy,
                0,
                SEAT_HEIGHT
            )

    # -------------------------
    # BACK SUPPORTS (2 uprights)
    # -------------------------
    support_x = half_w - LEG_THICKNESS

    for sx in (-1, 1):
        add_box(
            bm,
            sx * support_x,
            sx * support_x + LEG_THICKNESS * sx,
            half_d - LEG_THICKNESS,
            half_d,
            SEAT_HEIGHT,
            BACK_HEIGHT
        )

    # -------------------------
    # BACK PANEL
    # -------------------------
    add_box(
        bm,
        -half_w,
        half_w,
        half_d - BACK_THICKNESS,
        half_d,
        BACK_HEIGHT - 0.3,
        BACK_HEIGHT
    )

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    return obj


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    clear_scene()
    create_chair()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "chair.fbx"
    )

    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=False)
    print("Chair exported.")
import bpy
import bmesh
import os
import math

# -------------------------
# CONFIG
# -------------------------
SEAT_RADIUS = 0.35
SEAT_THICKNESS = 0.05
STOOL_HEIGHT = 0.5

LEG_RADIUS = 0.04
LEG_COUNT = 4
LEG_INSET = 0.06

SUPPORT_RING = True
RING_RADIUS = 0.18
RING_THICKNESS = 0.03

SEGMENTS = 32


# -------------------------
# UTIL
# -------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_stool():

    mesh = bpy.data.meshes.new("StoolMesh")
    obj = bpy.data.objects.new("Stool", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # -------------------------
    # SEAT (Cylinder)
    # -------------------------
    seat = bmesh.ops.create_circle(
        bm,
        segments=SEGMENTS,
        radius=SEAT_RADIUS
    )

    seat_verts = seat["verts"]
    seat_face = bm.faces.new(seat_verts)

    extrude = bmesh.ops.extrude_face_region(bm, geom=[seat_face])
    seat_ex = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

    bmesh.ops.translate(
        bm,
        verts=seat_ex,
        vec=(0, 0, -SEAT_THICKNESS)
    )

    # Move seat to final height
    bmesh.ops.translate(
        bm,
        verts=bm.verts,
        vec=(0, 0, STOOL_HEIGHT)
    )

    # -------------------------
    # LEGS
    # -------------------------
    leg_height = STOOL_HEIGHT

    leg_distance = SEAT_RADIUS - LEG_INSET

    for i in range(LEG_COUNT):

        angle = (2 * math.pi / LEG_COUNT) * i
        x = math.cos(angle) * leg_distance
        y = math.sin(angle) * leg_distance

        leg = bmesh.ops.create_circle(
            bm,
            segments=12,
            radius=LEG_RADIUS
        )

        leg_verts = leg["verts"]
        face = bm.faces.new(leg_verts)

        extrude = bmesh.ops.extrude_face_region(bm, geom=[face])
        leg_ex = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

        bmesh.ops.translate(
            bm,
            verts=leg_ex,
            vec=(0, 0, leg_height)
        )

        bmesh.ops.translate(
            bm,
            verts=leg_verts + leg_ex,
            vec=(x, y, 0)
        )

    # -------------------------
    # SUPPORT RING
    # -------------------------
    if SUPPORT_RING:

        ring = bmesh.ops.create_circle(
            bm,
            segments=SEGMENTS,
            radius=RING_RADIUS
        )

        ring_verts = ring["verts"]
        ring_face = bm.faces.new(ring_verts)

        extrude = bmesh.ops.extrude_face_region(bm, geom=[ring_face])
        ring_ex = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

        bmesh.ops.translate(
            bm,
            verts=ring_ex,
            vec=(0, 0, RING_THICKNESS)
        )

        # Place ring lower between legs
        bmesh.ops.translate(
            bm,
            verts=ring_verts + ring_ex,
            vec=(0, 0, STOOL_HEIGHT * 0.4)
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
    create_stool()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "stool.fbx"
    )

    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=False)

    print("Stool exported.")
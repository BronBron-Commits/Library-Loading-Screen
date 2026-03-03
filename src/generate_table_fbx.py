import bpy
import bmesh
import os
import math

# -------------------------
# CONFIG
# -------------------------
TABLE_RADIUS = 1.0
TABLE_THICKNESS = 0.08
TABLE_HEIGHT = 1.0

PEDESTAL_RADIUS = 0.15
BASE_RADIUS = 0.4
BASE_THICKNESS = 0.08

SEGMENTS = 48


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_table():

    mesh = bpy.data.meshes.new("CircularTableMesh")
    obj = bpy.data.objects.new("CircularTable", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # -------------------------
    # TABLETOP (Cylinder)
    # -------------------------
    top_geom = bmesh.ops.create_circle(
        bm,
        segments=SEGMENTS,
        radius=TABLE_RADIUS
    )

    top_verts = top_geom["verts"]

    # Create top face
    bm.faces.new(top_verts)

    # Extrude downward
    extrude = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    extruded_verts = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

    bmesh.ops.translate(
        bm,
        verts=extruded_verts,
        vec=(0, 0, -TABLE_THICKNESS)
    )

    # Move tabletop up to final height
    bmesh.ops.translate(
        bm,
        verts=bm.verts,
        vec=(0, 0, TABLE_HEIGHT)
    )

    # -------------------------
    # PEDESTAL (Cylinder)
    # -------------------------
    pedestal = bmesh.ops.create_circle(
        bm,
        segments=SEGMENTS,
        radius=PEDESTAL_RADIUS
    )

    pedestal_verts = pedestal["verts"]
    face = bm.faces.new(pedestal_verts)

    extrude = bmesh.ops.extrude_face_region(bm, geom=[face])
    ped_verts = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

    bmesh.ops.translate(
        bm,
        verts=ped_verts,
        vec=(0, 0, TABLE_HEIGHT - TABLE_THICKNESS)
    )

    # -------------------------
    # BASE (Cylinder)
    # -------------------------
    base = bmesh.ops.create_circle(
        bm,
        segments=SEGMENTS,
        radius=BASE_RADIUS
    )

    base_verts = base["verts"]
    face = bm.faces.new(base_verts)

    extrude = bmesh.ops.extrude_face_region(bm, geom=[face])
    base_verts_ex = [v for v in extrude["geom"] if isinstance(v, bmesh.types.BMVert)]

    bmesh.ops.translate(
        bm,
        verts=base_verts_ex,
        vec=(0, 0, BASE_THICKNESS)
    )

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    return obj


if __name__ == "__main__":
    clear_scene()
    create_table()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "circular_table.fbx"
    )

    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=False)

    print("Circular table exported.")
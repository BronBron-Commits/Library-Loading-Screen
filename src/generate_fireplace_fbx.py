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


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_fireplace():

    mesh = bpy.data.meshes.new("FireplaceMesh")
    obj = bpy.data.objects.new("Fireplace", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    half_w = WIDTH / 2
    half_d = DEPTH / 2
    opening_w = WIDTH - 2 * FRAME

    # -------------------------
    # Create Front Frame Ring (2D profile)
    # -------------------------

    # Outer rectangle
    v1 = bm.verts.new((-half_w, 0, 0))
    v2 = bm.verts.new(( half_w, 0, 0))
    v3 = bm.verts.new(( half_w, 0, HEIGHT))
    v4 = bm.verts.new((-half_w, 0, HEIGHT))

    # Inner opening
    v5 = bm.verts.new((-opening_w/2, 0, 0))
    v6 = bm.verts.new(( opening_w/2, 0, 0))
    v7 = bm.verts.new(( opening_w/2, 0, OPENING_HEIGHT))
    v8 = bm.verts.new((-opening_w/2, 0, OPENING_HEIGHT))

    # Create faces around opening (frame ring)
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v4, v8, v7])
    bm.faces.new([v4, v1, v5, v8])

    # -------------------------
    # Extrude Frame Backward
    # -------------------------

    geom = bm.faces[:]
    ret = bmesh.ops.extrude_face_region(bm, geom=geom)
    verts_extruded = [ele for ele in ret["geom"] if isinstance(ele, bmesh.types.BMVert)]

    # Move extruded geometry back in Y
    bmesh.ops.translate(
        bm,
        verts=verts_extruded,
        vec=(0, -DEPTH, 0)
    )

    # -------------------------
    # Add Back Wall Inside Opening
    # -------------------------

    # Get inner back verts
    back_z = 0
    back_top = OPENING_HEIGHT

    v9  = bm.verts.new((-opening_w/2, -DEPTH, back_z))
    v10 = bm.verts.new(( opening_w/2, -DEPTH, back_z))
    v11 = bm.verts.new(( opening_w/2, -DEPTH, back_top))
    v12 = bm.verts.new((-opening_w/2, -DEPTH, back_top))

    bm.faces.new([v9, v10, v11, v12])

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    return obj


if __name__ == "__main__":
    clear_scene()
    create_fireplace()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "fireplace_clean.fbx"
    )

    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=False)
    print("Clean fireplace exported.")
import bpy
import bmesh
import os

# -------------------------
# CONFIG
# -------------------------
WIDTH = 2.0
HEIGHT = 2.5
DEPTH = 0.3
THICKNESS = 0.05
NUM_SHELVES = 4


# -------------------------
# UTIL
# -------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def add_box(bm, x_min, x_max, y_min, y_max, z_min, z_max):
    """Add a box to a bmesh using coordinate bounds."""

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
# BOOKSHELF
# -------------------------
def create_bookshelf():

    mesh = bpy.data.meshes.new("BookshelfMesh")
    obj = bpy.data.objects.new("Bookshelf", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # ---- Sides ----
    add_box(
        bm,
        -WIDTH/2,
        -WIDTH/2 + THICKNESS,
        -DEPTH/2,
        DEPTH/2,
        0,
        HEIGHT
    )

    add_box(
        bm,
        WIDTH/2 - THICKNESS,
        WIDTH/2,
        -DEPTH/2,
        DEPTH/2,
        0,
        HEIGHT
    )

    # ---- Bottom ----
    add_box(
        bm,
        -WIDTH/2 + THICKNESS,
        WIDTH/2 - THICKNESS,
        -DEPTH/2,
        DEPTH/2,
        0,
        THICKNESS
    )

    # ---- Top ----
    add_box(
        bm,
        -WIDTH/2 + THICKNESS,
        WIDTH/2 - THICKNESS,
        -DEPTH/2,
        DEPTH/2,
        HEIGHT - THICKNESS,
        HEIGHT
    )

    # ---- Interior Shelves ----
    interior_height = HEIGHT - 2 * THICKNESS
    spacing = interior_height / (NUM_SHELVES + 1)

    for i in range(NUM_SHELVES):
        z = THICKNESS + spacing * (i + 1)

        add_box(
            bm,
            -WIDTH/2 + THICKNESS,
            WIDTH/2 - THICKNESS,
            -DEPTH/2,
            DEPTH/2,
            z,
            z + THICKNESS
        )

    # Finalize mesh
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
    create_bookshelf()

    export_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "bookshelf.fbx"
    )

    export_fbx(export_path)
    print(f"Exported bookshelf to {export_path}")
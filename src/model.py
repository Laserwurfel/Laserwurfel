import pyassimp


def import_asset(file):
    scene = pyassimp.load(file)

    assert len(scene.meshes)
    mesh = scene.meshes[0]

    assert len(mesh.vertices)
    print(mesh.vertices[0])

    # don't forget this one, or you will leak!
    pyassimp.release(scene)

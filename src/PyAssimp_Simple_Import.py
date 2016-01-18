import pyassimp

def import_asset(file):

	scene = load(file)

	assert len(scene.meshes)
	mesh = scene.meshes[0]

	assert len(mesh.vertices)
	print(mesh.vertices[0])

	# don't forget this one, or you will leak!
	release(scene)
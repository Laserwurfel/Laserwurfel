# TODO better name
def path(cube, source, goal):
    """Creates two linked start and end points"""
    pass


def deactivate(cube, point):
    """Deactivates a node"""
    pass


def connection(cube, point_from, point_to):
    """Creates a permanent connection between two points"""
    pass


def wall(cube, block_from, block_to, *switch_pairs):
    """Creates a wall between two points and optional switches between
    additional pairs of points"""
    pass


def teleporter(cube, point_from, point_to):
    """Creates a teleporter connection between two points"""
    pass

from __future__ import unicode_literals

import re

from . import structure


RE_EMPTY = re.compile(r'^\s*$')
RE_META = re.compile(r'^([a-zA-Z])\s*:\s*(.*)$')
RE_META_VALUES = {
    'string': re.compile(r'^"[a-zA-Z0-9 ]"$'),
    'path': re.compile(r'^\.(?:/[^\s]+)+'),
}
RE_STRUCTURE_FUNCTION = re.compile(r'^([^\s]+)\s+')
RE_STRUCTURE_POINT = re.compile(r'[a-z]+_[a-z]+(?:[a-z])?')
POINT_AXES = [
    ['front', 'back'],
    ['left', 'right'],
    ['up', 'down'],
]

STRUCTURE_FUNCTIONS = {
    '*': structure.path,
    '!': structure.deactivate,
    '--': structure.connection,
    '[]': structure.wall,
    '%': structure.teleporter,
}


def parse(file):
    level = {
        'meta': {},
        'detail': {
            'front': {},
            'back': {},
            'left': {},
            'right': {},
            'up': {},
            'down': {},
        },
        'structure': [],
    }

    # parse level
    with open(file, 'r') as f:
        # meta
        for line in f:
            if RE_EMPTY.match(line):
                break
            match = RE_META.match(line)
            if match is None:
                raise ValueError("Encountered invalid meta line", line)
            (key, value) = match.groups()

            # check if type has known value type
            for type in RE_META_VALUES:
                if RE_META_VALUES[type].match(value):
                    # TODO extract value
                    break
            else:
                raise TypeError(
                    "Meta-key `{}` has unknown value `{}`".format(key, value)
                )

            # check if key already exists
            if key in level.meta:
                raise ValueError(
                    "Meta-key `{}` has already been defined".format(key)
                )

        # details
        # TODO implement parsing

        # structure
        for line in f:
            # get function
            match = RE_STRUCTURE_FUNCTION.match(line)
            if match is None:
                raise ValueError("Encountered invalid structure line", line)
            structure_function = match.group(0)
            if structure_function not in STRUCTURE_FUNCTIONS:
                raise ValueError(
                    "Structure-function `{}` is unknown".format()
                )

            # get points
            structure_entry = [structure_function]
            for match in RE_STRUCTURE_POINT.finditer(line, match.end(0)):
                if match is None:
                    raise ValueError("Structure entry has invalid point", line)
                point = match.group(0)

                # TODO parse point
                parts = point.split('_')
                if parts[0] in POINT_AXES[0]:
                    if parts[1] in POINT_AXES[1]:
                        if len(parts) == 2:
                            # axes 1 2
                            pass
                        elif parts[2] not in POINT_AXES[2]:
                            raise ValueError(
                                "Expected axis 3 after axes 1, 2",
                                point
                            )
                        else:
                            # axes 1 2 3
                            pass
                    elif parts[1] in POINT_AXES[2]:
                        if len(parts) != 2:
                            raise ValueError(
                                "Found too many parts after axes 1, 3",
                                point
                            )
                        else:
                            # axes 1 3
                            pass
                elif parts[0] in POINT_AXES[1]:
                    if len(parts) != 2:
                        raise ValueError(
                            "Found too many parts after axis 2",
                            point
                        )
                    elif parts[1] not in POINT_AXES[2]:
                        raise ValueError(
                            "Expected axis 3 after axis 2",
                            point
                        )
                    else:
                        # axes 2 3
                        pass
                else:
                    raise ValueError(
                        "Expected axis 1 or 2 at beginning",
                        point
                    )

                structure_entry.append(point)

            level.structure.append(structure_entry)

    return level

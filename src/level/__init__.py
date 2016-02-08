from __future__ import unicode_literals

import re

from . import structure


RE_EMPTY = re.compile(r'^\s*$')

RE_META = re.compile(r'^([a-zA-Z]+)+\s*:\s*(.*)$')
RE_META_VALUES = {
    'string': re.compile(r'^"[^"]+"$'),
    'path': re.compile(r'^\.(?:/[^/]+)+'),
}

DETAIL_SHORT_INDENT = ' ' * (1 + (9*2))
DETAIL_DELIMITER_LINE = ('--' * 4) + r'\(\)' + ('--' * 4)
DETAIL_COLUMNS = '(..)' * 9
RE_DETAIL_SHORT_DELIMITER = re.compile(
    r'^' +
    DETAIL_SHORT_INDENT +
    r'O' +
    DETAIL_DELIMITER_LINE +
    r'O$'
)
RE_DETAIL_SHORT_CENTER = re.compile(
    '^' +
    DETAIL_SHORT_INDENT +
    r'O' +
    DETAIL_COLUMNS +
    'O$'
)
RE_DETAIL_SHORT = re.compile(
    '^' +
    DETAIL_SHORT_INDENT +
    r'\|' +
    DETAIL_COLUMNS +
    '\|$'
)
RE_DETAIL_LONG_DELIMITER = re.compile(
    r'^O(?:' +
    DETAIL_DELIMITER_LINE +
    r'O){4}'
)
RE_DETAIL_LONG_CENTER = re.compile(
    DETAIL_COLUMNS + r'O'
)
RE_DETAIL_LONG = re.compile(
    DETAIL_COLUMNS + r'\|'
)
DETAIL_LONG_SIDES = ['left', 'front', 'right', 'back']

RE_STRUCTURE_FUNCTION = re.compile(r'^([^\s]+)\s+')
RE_STRUCTURE_POINT = re.compile(r'[a-z]+_[a-z]+(?:_[a-z]+)?')
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


class Level:
    def __init__(self, path):
        self.meta = {}
        self.detail = {
            'front': [],
            'back': [],
            'left': [],
            'right': [],
            'up': [],
            'down': [],
        }
        self.structure = []

        # parse level
        with open(path, 'r') as f:
            line_number = 0

            try:

                # META #

                while True:
                    line = f.next()
                    line_number += 1

                    if RE_EMPTY.match(line):
                        break
                    match = RE_META.match(line)
                    if match is None:
                        raise ValueError(
                            "Encountered invalid meta line",
                            line_number,
                        )
                    (key, value) = match.groups()

                    # check if type has known value type
                    for k in RE_META_VALUES:
                        if RE_META_VALUES[k].match(value):
                            # TODO extract value
                            break
                    else:
                        raise TypeError(
                            "Meta-key '{}' has unknown value '{}'"
                            .format(key, value),
                            line_number,
                        )

                    # check if key already exists
                    if key in self.meta:
                        raise ValueError(
                            "Meta-key '{}' has already been defined"
                            .format(key),
                            line_number,
                        )

                    self.meta[key] = value

                # DETAILS #

                # short delimiter
                line = f.next()
                line_number += 1
                if not RE_DETAIL_SHORT_DELIMITER.match(line):
                    raise ValueError("Expected edge on line", line_number)

                # 4 normal short details
                for i in range(4):
                    line = f.next()
                    line_number += 1
                    match = RE_DETAIL_SHORT.match(line)
                    if match is None:
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )
                    self.detail['up'].append(match.groups())

                # center short details
                line = f.next()
                line_number += 1
                match = RE_DETAIL_SHORT_CENTER.match(line)
                if match is None:
                    raise ValueError("Expected details on line", line_number)
                self.detail['up'].append(match.groups())

                # 4 normal short details
                for i in range(4):
                    line = f.next()
                    line_number += 1
                    match = RE_DETAIL_SHORT.match(line)
                    if match is None:
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )
                    self.detail['up'].append(match.groups())

                # long delimiter
                line = f.next()
                line_number += 1
                if not RE_DETAIL_LONG_DELIMITER.match(line):
                    raise ValueError("Expected edge on line", line_number)

                # 4 normal long details
                for i in range(4):
                    line = f.next()
                    line_number += 1

                    if not re.match('^|', line):
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )

                    start = 1
                    for side in DETAIL_LONG_SIDES:
                        match = RE_DETAIL_LONG.match(line, start)
                        if match is None:
                            raise ValueError(
                                "Expected details on line",
                                line_number,
                            )
                        self.detail[side].append(match.groups())
                        start = match.end(0)

                    if not re.match('|$', line, start):
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )

                # center long details
                line = f.next()
                line_number += 1

                if not re.match('^|', line):
                    raise ValueError(
                        "Expected details on line",
                        line_number,
                    )

                start = 1
                for side in DETAIL_LONG_SIDES:
                    match = RE_DETAIL_LONG_CENTER.match(line, start)
                    if match is None:
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )
                    self.detail[side].append(match.groups())
                    start = match.end(0)

                if not re.match('|$', line, start):
                    raise ValueError(
                        "Expected details on line",
                        line_number,
                    )

                # 4 normal long details
                for i in range(4):
                    line = f.next()
                    line_number += 1

                    if not re.match('^|', line):
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )

                    start = 1
                    for side in DETAIL_LONG_SIDES:
                        match = RE_DETAIL_LONG.match(line, start)
                        if match is None:
                            raise ValueError(
                                "Expected details on line",
                                line_number,
                            )
                        self.detail[side].append(match.groups())
                        start = match.end(0)

                    if not re.match('|$', line, start):
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )

                # long delimiter
                line = f.next()
                line_number += 1
                if not RE_DETAIL_LONG_DELIMITER.match(line):
                    raise ValueError("Expected edge on line", line_number)

                # 4 normal short details
                for i in range(4):
                    line = f.next()
                    line_number += 1
                    match = RE_DETAIL_SHORT.match(line)
                    if match is None:
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )
                    self.detail['down'].append(match.groups())

                # center short details
                line = f.next()
                line_number += 1
                match = RE_DETAIL_SHORT_CENTER.match(line)
                if match is None:
                    raise ValueError("Expected details on line", line_number)
                self.detail['down'].append(match.groups())

                # 4 normal short details
                for i in range(4):
                    line = f.next()
                    line_number += 1
                    match = RE_DETAIL_SHORT.match(line)
                    if match is None:
                        raise ValueError(
                            "Expected details on line",
                            line_number,
                        )
                    self.detail['down'].append(match.groups())

                # short delimiter
                line = f.next()
                line_number += 1
                if not RE_DETAIL_SHORT_DELIMITER.match(line):
                    raise ValueError("Expected edge on line", line_number)

                line = f.next()
                line_number += 1
                if not RE_EMPTY.match(line):
                    raise ValueError("Expected empty line", line_number)
            except StopIteration:
                raise EOFError("Unexpected end of file")

                # STRUCTURE #

            try:
                while True:
                    line = f.next()
                    line_number += 1

                    if RE_EMPTY.match(line):
                        continue

                    # get function
                    match = RE_STRUCTURE_FUNCTION.match(line)
                    if match is None:
                        raise ValueError(
                            "Encountered invalid structure line",
                            line_number,
                        )
                    structure_function = match.group(1)
                    if structure_function not in STRUCTURE_FUNCTIONS:
                        raise ValueError(
                            "Structure-function '{}' is unknown"
                            .format(structure_function),
                            line_number,
                        )

                    # get points
                    structure_entry = [structure_function]
                    for match in RE_STRUCTURE_POINT.finditer(
                            line,
                            match.end(0),
                    ):
                        if match is None:
                            raise ValueError(
                                "Structure entry has invalid point",
                                line_number,
                            )
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
                                        point,
                                        line_number,
                                    )
                                else:
                                    # axes 1 2 3
                                    pass
                            elif parts[1] in POINT_AXES[2]:
                                if len(parts) != 2:
                                    raise ValueError(
                                        "Found too many parts after axes 1, 3",
                                        point,
                                        line_number,
                                    )
                                else:
                                    # axes 1 3
                                    pass
                        elif parts[0] in POINT_AXES[1]:
                            if len(parts) != 2:
                                raise ValueError(
                                    "Found too many parts after axis 2",
                                    point,
                                    line_number,
                                )
                            elif parts[1] not in POINT_AXES[2]:
                                raise ValueError(
                                    "Expected axis 3 after axis 2",
                                    point,
                                    line_number,
                                )
                            else:
                                # axes 2 3
                                pass
                        else:
                            raise ValueError(
                                "Expected axis 1 or 2 at beginning",
                                point,
                                line_number,
                            )

                        structure_entry.append(point)

                    # TODO check argument count with inspection
                    self.structure.append(structure_entry)
            except StopIteration:
                pass
from __future__ import unicode_literals

import re
import inspect

from . import structure


RE_EMPTY = re.compile(r'^\s*$')

RE_META = re.compile(r'^([a-zA-Z]+)+\s*:\s*(.*)$')
RE_META_VALUES = {
    'string': re.compile(r'^"([^"]*)"$'),
    'path': re.compile(r'^(\.{0,2}(?:/[^/]+)+)$'),
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
    ['bottom', 'top'],
]
STRUCTURE_FUNCTIONS = {
    '*': structure.path,
    '!': structure.deactivate,
    '--': structure.connection,
    '[]': structure.wall,
    '%': structure.teleporter,
}


def _gen_detail():
    return {
        'front': _gen_detail_side(),
        'back': _gen_detail_side(),
        'left': _gen_detail_side(),
        'right': _gen_detail_side(),
        'top': _gen_detail_side(),
        'bottom': _gen_detail_side(),
    }


def _gen_detail_side():
    return [[None] * 9 for _ in range(9)]


class Level:
    def __init__(self):
        self.meta = {}
        self.detail = _gen_detail()
        self.structure = []

    def parse(self, path):
        with open(path, 'r') as f:
            try:
                self.meta = parse_meta(f)
            except StopIteration:
                raise EOFError("Unexpected end of file")

            self.detail = parse_detail(f)

            self.structure = parse_structure(f)


def parse_meta(lines):
    meta = {}

    for line in lines:
        if RE_EMPTY.match(line):
            break
        match = RE_META.match(line)
        if match is None:
            raise ValueError(
                "Encountered invalid meta line",
                line,
            )
        (key, value) = match.groups()

        # check if type has known value type
        for k in RE_META_VALUES:
            match = RE_META_VALUES[k].match(value)
            if match is not None:
                # extract value and pass along type information
                value = (
                    k,
                    match.group(1),
                )
                break
        else:
            raise TypeError(
                "Meta-key '{}' has unknown value '{}'"
                .format(key, value),
                line,
            )

        # check if key already exists
        if key in meta:
            raise ValueError(
                "Meta-key '{}' has already been defined"
                .format(key),
                line,
            )

        meta[key] = value

    return meta


def parse_detail(lines):
    details = _gen_detail()

    try:
        # short delimiter
        line = lines.next()
        if not RE_DETAIL_SHORT_DELIMITER.match(line):
            raise ValueError("Expected edge", line)

        # 4 normal short details
        for row in range(4):
            line = lines.next()
            match = RE_DETAIL_SHORT.match(line)
            if match is None:
                raise ValueError("Expected details", lines)
            for column, detail in enumerate(match.groups()):
                if not detail.strip():
                    continue
                details['top'][8-row][column] = detail

        # center short details
        line = lines.next()
        match = RE_DETAIL_SHORT_CENTER.match(line)
        if match is None:
            raise ValueError("Expected details", line)
        for column, detail in enumerate(match.groups()):
            if not detail.strip():
                continue
            details['top'][8-4][column] = detail

        # 4 normal short details
        for row in range(4):
            line = lines.next()
            match = RE_DETAIL_SHORT.match(line)
            if match is None:
                raise ValueError("Expected details", line)
            for column, detail in enumerate(match.groups()):
                if detail.strip():
                    details['top'][8-5-row][column] = detail

        # long delimiter
        line = lines.next()
        if not RE_DETAIL_LONG_DELIMITER.match(line):
            raise ValueError("Expected edge", line)

        # 4 normal long details
        for row in range(4):
            line = lines.next()

            if not re.match('^|', line):
                raise ValueError("Expected details", line)

            start = 1
            for side in DETAIL_LONG_SIDES:
                match = RE_DETAIL_LONG.match(line, start)
                if match is None:
                    raise ValueError("Expected details", line)
                for column, detail in enumerate(match.groups()):
                    if not detail.strip():
                        continue
                    elif side == 'left':
                        details[side][8-row][8-column] = detail
                    elif side == 'front':
                        details[side][8-row][column] = detail
                    elif side == 'right':
                        details[side][8-row][column] = detail
                    elif side == 'back':
                        details[side][8-row][8-column] = detail
                start = match.end(0)

            if not re.match('|$', line, start):
                raise ValueError("Expected details", line)

        # center long details
        line = lines.next()

        if not re.match('^|', line):
            raise ValueError("Expected details", line)

        start = 1
        for side in DETAIL_LONG_SIDES:
            match = RE_DETAIL_LONG_CENTER.match(line, start)
            if match is None:
                raise ValueError("Expected details", line)
            for column, detail in enumerate(match.groups()):
                if not detail.strip():
                    continue
                if side == 'left':
                    details[side][8-4][8-column] = detail
                elif side == 'front':
                    details[side][8-4][column] = detail
                elif side == 'right':
                    details[side][8-4][column] = detail
                elif side == 'back':
                    details[side][8-4][8-column] = detail
            start = match.end(0)

        if not re.match('|$', line, start):
            raise ValueError("Expected details", line)

        # 4 normal long details
        for row in range(4):
            line = lines.next()

            if not re.match('^|', line):
                raise ValueError("Expected details", line)

            start = 1
            for side in DETAIL_LONG_SIDES:
                match = RE_DETAIL_LONG.match(line, start)
                if match is None:
                    raise ValueError("Expected details", line)
                for column, detail in enumerate(match.groups()):
                    if not detail.strip():
                        continue
                    if side == 'left':
                        details[side][8-5-row][8-column] = detail
                    elif side == 'front':
                        details[side][8-5-row][column] = detail
                    elif side == 'right':
                        details[side][8-5-row][column] = detail
                    elif side == 'back':
                        details[side][8-5-row][8-column] = detail
                start = match.end(0)

            if not re.match('|$', line, start):
                raise ValueError("Expected details", line)

        # long delimiter
        line = lines.next()
        if not RE_DETAIL_LONG_DELIMITER.match(line):
            raise ValueError("Expected edge", line)

        # 4 normal short details
        for row in range(4):
            line = lines.next()
            match = RE_DETAIL_SHORT.match(line)
            if match is None:
                raise ValueError("Expected details", line)
            for column, detail in enumerate(match.groups()):
                if not detail.strip():
                    continue
                details['bottom'][row][column] = detail

        # center short details
        line = lines.next()
        match = RE_DETAIL_SHORT_CENTER.match(line)
        if match is None:
            raise ValueError("Expected details", line)
        for column, detail in enumerate(match.groups()):
            if not detail.strip():
                continue
            details['bottom'][4][column] = detail

        # 4 normal short details
        for row in range(4):
            line = lines.next()
            match = RE_DETAIL_SHORT.match(line)
            if match is None:
                raise ValueError("Expected details", line)
            for column, detail in enumerate(match.groups()):
                if not detail.strip():
                    continue
                details['bottom'][5+row][column] = detail

        # short delimiter
        line = lines.next()
        if not RE_DETAIL_SHORT_DELIMITER.match(line):
            raise ValueError("Expected edge", line)
    except StopIteration:
        raise EOFError("Unexpected end of file")

    return details


def parse_structure(lines):
    structures = []

    for line in lines:
        if RE_EMPTY.match(line):
            continue

        # get function
        match = RE_STRUCTURE_FUNCTION.match(line)
        if match is None:
            raise ValueError("Encountered invalid structure", line)
        structure_function = match.group(1)
        if structure_function not in STRUCTURE_FUNCTIONS:
            raise ValueError(
                "Structure-function '{}' is unknown"
                .format(structure_function),
                line,
            )
        structure_function = STRUCTURE_FUNCTIONS[structure_function]
        structure_entry = [structure_function]

        # get points
        for match in RE_STRUCTURE_POINT.finditer(
                line,
                match.end(0),
        ):
            if match is None:
                raise ValueError(
                    "Structure entry has invalid point",
                    line,
                )

            point = match.group(0)
            parts = point.split('_')

            if parts[0] in POINT_AXES[0]:
                if parts[1] in POINT_AXES[1]:
                    if len(parts) == 2:
                        # axes 1 2
                        point = (parts[0], parts[1], 0)
                    elif parts[2] not in POINT_AXES[2]:
                        raise ValueError(
                            "Expected axis 3 after axes 1, 2",
                            point,
                            line,
                        )
                    else:
                        # axes 1 2 3
                        point = (parts[0], parts[1], parts[2])
                elif parts[1] in POINT_AXES[2]:
                    if len(parts) != 2:
                        raise ValueError(
                            "Found too many parts after axes 1, 3",
                            point,
                            line,
                        )
                    else:
                        # axes 1 3
                        point = (parts[0], 0, parts[1])
            elif parts[0] in POINT_AXES[1]:
                if len(parts) != 2:
                    raise ValueError(
                        "Found too many parts after axis 2",
                        point,
                        line,
                    )
                elif parts[1] not in POINT_AXES[2]:
                    raise ValueError(
                        "Expected axis 3 after axis 2",
                        point,
                        line,
                    )
                else:
                    # axes 2 3
                    point = (0, parts[0], parts[1])
            else:
                raise ValueError(
                    "Expected axis 1 or 2 at beginning",
                    point,
                    line,
                )

            # parse point
            point = tuple(
                (
                    -1
                    if POINT_AXES[i].index(x) == 0
                    else
                    1
                )
                if type(x) == unicode
                else x
                for i, x in enumerate(point)
            )

            # convert roll/pitch/yaw to x/y/z
            structure_entry.append((
                point[1],
                point[0],
                point[2],
            ))

        # check argument count
        # both length are 1 above the actual count
        expected = len(inspect.getargspec(structure_entry[0])[0])
        actual = len(structure_entry)
        if expected != actual:
            raise ValueError(
                "Expected {} arguments for structure entry, got {}"
                .format(expected, actual),
                line,
                line
            )

        structures.append(tuple(structure_entry))

    return structures
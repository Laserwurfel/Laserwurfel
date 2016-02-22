from .. import level
import unittest
import os.path


class StandardLevelTestCase(unittest.TestCase):
    def setUp(self):
        self.here = os.path.abspath(os.path.dirname(__file__))

    def test_full(self):
        full = level.Level()
        full.parse(os.path.join(self.here, 'level/full'))

    def test_meta(self):
        with open(os.path.join(self.here, 'level/meta')) as f:
            meta = level.parse_meta(f)
            self.assertDictEqual(
                meta,
                {
                    "title": ("string", "Test Level"),
                    "track": ("path", "./assets/music/OGG files/lvl 1.ogg"),
                },
            )

    def test_structure(self):
        with open(os.path.join(self.here, 'level/structure')) as f:
            structure = level.parse_structure(f)
            self.assertEqual(
                structure,
                [
                    (
                        level.structure.path,
                        (-1, -1, +1),
                        (+1, -1, -1),
                    ),
                    (
                        level.structure.deactivate,
                        (-1, 00, +1),
                    ),
                    (
                        level.structure.connection,
                        (+1, 00, +1),
                        (+1, 00, -1),
                    ),
                    (
                        level.structure.wall,
                        (+1, -1, 00),
                        (+1, -1, -1),
                    ),
                    (
                        level.structure.teleporter,
                        (-1, +1, +1),
                        (00, +1, -1),
                    ),
                ],
            )

    def test_detail(self):
        with open(os.path.join(self.here, 'level/detail')) as f:
            detail = level.parse_detail(f)
            self.assertEqual(
                detail['front'],
                [
                    ["bl", None, None, None, None, None, None, None, "br"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["tl", None, None, None, None, None, None, None, "tr"],
                ],
                "front details different",
            )
            self.assertEqual(
                detail['back'],
                [
                    ["br", None, None, None, None, None, None, None, "bl"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["tr", None, None, None, None, None, None, None, "tl"],
                ],
                "back details different",
            )
            self.assertEqual(
                detail['left'],
                [
                    ["br", None, None, None, None, None, None, None, "bl"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["tr", None, None, None, None, None, None, None, "tl"],
                ],
                "left details different",
            )
            self.assertEqual(
                detail['right'],
                [
                    ["bl", None, None, None, None, None, None, None, "br"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["tl", None, None, None, None, None, None, None, "tr"],
                ],
                "right details different",
            )
            self.assertEqual(
                detail['bottom'],
                [
                    ["tl", None, None, None, None, None, None, None, "tr"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["bl", None, None, None, None, None, None, None, "br"],
                ],
                "bottom details different",
            )
            self.assertEqual(
                detail['top'],
                [
                    ["bl", None, None, None, None, None, None, None, "br"],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None],
                    ["tl", None, None, None, None, None, None, None, "tr"],
                ],
                "top details different",
            )


class BrokenDetailTestCase(unittest.TestCase):
    def setUp(self):
        self.here = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'level/details',
        )

    @unittest.expectedFailure
    def test_7x7(self):
        with open(os.path.join(self.here, '7x7')) as f:
            level.parse_detail(f)

    @unittest.expectedFailure
    def test_missing_column(self):
        with open(os.path.join(self.here, 'missing_column')) as f:
            level.parse_detail(f)

    @unittest.expectedFailure
    def test_missing_delimiter_long(self):
        with open(os.path.join(self.here, 'missing_delimiter_long')) as f:
            level.parse_detail(f)

    @unittest.expectedFailure
    def test_missing_delimiter_short(self):
        with open(os.path.join(self.here, 'missing_delimiter_short')) as f:
            level.parse_detail(f)

    @unittest.expectedFailure
    def test_missing_edge(self):
        with open(os.path.join(self.here, 'missing_edge')) as f:
            level.parse_detail(f)


class BrokenStructureTestCase(unittest.TestCase):
    def setUp(self):
        self.here = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'level/structures',
        )

    @unittest.expectedFailure
    def test_invalid_points(self):
        with open(os.path.join(self.here, 'invalid_points')) as f:
            level.parse_structure(f)

    @unittest.expectedFailure
    def test_no_arguments(self):
        with open(os.path.join(self.here, 'no_arguments')) as f:
            level.parse_structure(f)

    @unittest.expectedFailure
    def test_unkown_function(self):
        with open(os.path.join(self.here, 'unknown_function')) as f:
            level.parse_structure(f)

    @unittest.expectedFailure
    def test_wrong_arguments(self):
        with open(os.path.join(self.here, 'wrong_arguments')) as f:
            level.parse_structure(f)

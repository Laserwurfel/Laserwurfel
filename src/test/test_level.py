from .. import level
import unittest
import os.path


class StandardLevelTestCase(unittest.TestCase):
    def setUp(self):
        self.here = os.path.abspath(os.path.dirname(__file__))

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

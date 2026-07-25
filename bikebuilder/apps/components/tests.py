from django.test import SimpleTestCase

from .models import ShellType
from .parsers import parse_bb_shell


class ParseBBShellTests(SimpleTestCase):
    def test_splits_type_and_width(self):
        self.assertEqual(parse_bb_shell("BSA 68mm"), (ShellType.THREADED_BSA, 68))

    def test_aliases_map_to_same_type(self):
        self.assertEqual(
            parse_bb_shell("English threaded 68 mm")[0],
            parse_bb_shell("BSA/English 68mm")[0],
        )

    def test_italian_and_t47(self):
        self.assertEqual(parse_bb_shell("Italian 70mm"), (ShellType.THREADED_ITA, 70))
        self.assertEqual(parse_bb_shell("T47 86mm"), (ShellType.T47, 86))

    def test_range_takes_first_width(self):
        self.assertEqual(parse_bb_shell("BSA 68/73mm"), (ShellType.THREADED_BSA, 68))

    def test_unknown_shell_raises(self):
        with self.assertRaises(ValueError):
            parse_bb_shell("Widget Shell 68mm")

    def test_missing_width_raises(self):
        with self.assertRaises(ValueError):
            parse_bb_shell("BSA")

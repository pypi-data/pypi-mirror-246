import unittest
from os.path import join
from os import getcwd
from ..src.pathmr import Pathmr


class TestPathmr(unittest.TestCase):
    def test_pathmr_initialize(self):
        path = Pathmr('.')
        self.assertEqual(getcwd(), path.root)
        self.assertEqual(getcwd(), path)

    def test_absolute_join(self):
        path = Pathmr('test-dir/one/', 'two-a/../two-b/three-b')
        self.assertEqual(join(getcwd(), 'test-dir', 'one', 'two-b', 'three-b'), path)

    def test_magic_methods(self):
        path = Pathmr('test-dir/one/')
        self.assertEqual(path + 'two-a', join(getcwd(), 'test-dir', 'one', 'two-a'))
        self.assertEqual(path - 'one', join(getcwd(), 'test-dir'))
        self.assertEqual(~ path, join(getcwd(), 'test-dir'))

    def test_file_methods(self):
        path = Pathmr.resolve("test-dir/one/two-a/three-a/four-a/five.bin")
        self.assertTrue(path.isfile())
        self.assertFalse(path.isder())
        self.assertEqual(path.basename, "five")
        self.assertEqual(path.ext, "bin")


if __name__ == '__main__':
    unittest.main()

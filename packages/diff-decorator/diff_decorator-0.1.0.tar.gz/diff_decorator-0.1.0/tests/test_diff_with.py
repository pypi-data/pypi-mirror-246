import unittest
from unittest.mock import patch
from diff_decorator import diff_with

class TestDiffWithDecorator(unittest.TestCase):

    @patch('diff_decorator.diff_with.subprocess.run')
    def test_failed_default(self, mock_run):
        expected = "Hello\nWorld\n"
        actual = "Hello\nUniverse\n"
        with self.assertRaises(AssertionError):
            diff_with()(self.assertEqual)(expected, actual)
        mock_run.assert_called_once()

    @patch('diff_decorator.diff_with.subprocess.run')
    def test_failed_custom(self, mock_run):
        expected = "Hello\nAll\n"
        actual = "Hello\nEveryone\n"
        with self.assertRaises(AssertionError):
            diff_with(tool='meld')(self.assertEqual)(expected, actual)
        mock_run.assert_called_once_with(['meld', unittest.mock.ANY, unittest.mock.ANY])

    @patch('diff_decorator.diff_with.subprocess.run')
    def test_passed(self, mock_run):
        expected = "Hello\nWorld\n"
        actual = "Hello\nWorld\n"
        diff_with()(self.assertEqual)(expected, actual)
        mock_run.assert_not_called()

if __name__ == "__main__":
    unittest.main()


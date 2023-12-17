from io import StringIO
import mock
import unittest

import dotscanner.ui.window as ui

SMALL_WINDOW_WARNING = """
WARNING: Due to the device's screen size or the window height that has been manually selected, the \
window height will be smaller than 650 pixels for the threshold-adjustment and region-selection \
windows, potentially resulting in some buttons not being visible. However, the Return key will \
still allow confirmation in each window, and the Escape key will allow for skipping files, when \
the option is available.
"""


class TestWindow(unittest.TestCase):
    @mock.patch("settings.config.DYNAMIC_WINDOW", True)
    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_getWindowDimensions_dynamic(self, mock_stdout):
        width, height = ui.getWindowDimensions(600, 800)

        self.assertEqual(width, 508)
        self.assertEqual(height, 420)
        self.assertEqual(mock_stdout.getvalue(), SMALL_WINDOW_WARNING)

        width2, height2 = ui.getWindowDimensions(1600, 2560)

        self.assertEqual(width2, 1508)
        self.assertEqual(height2, 1420)

    @mock.patch("settings.config.DYNAMIC_WINDOW", False)
    @mock.patch("settings.config.WINDOW_HEIGHT", 650)
    @mock.patch("settings.config.WINDOW_WIDTH", 750)
    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_getWindowDimensions_notDynamic(self, mock_stdout):
        width, height = ui.getWindowDimensions(600, 800)

        self.assertEqual(width, 750)
        self.assertEqual(height, 650)
        self.assertNotEqual(mock_stdout.getvalue(), SMALL_WINDOW_WARNING)

        width2, height2 = ui.getWindowDimensions(1600, 2560)

        self.assertEqual(width, 750)
        self.assertEqual(height, 650)


if __name__ == '__main__':
    unittest.main()

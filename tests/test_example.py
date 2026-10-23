import contextlib
import importlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

import example_project
import example_project.main as main_module

# whocalled() reports on whatever script is running as __main__, so we pretend it is this one
FAKE_SCRIPT = Path("/some/folder/fake_script.py")


def capture_output(func, *args, **kwargs):
    """Run func and return everything it printed to the terminal."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue()


class TestExample(unittest.TestCase):
    def test_function(self):
        output = capture_output(example_project.function)
        self.assertEqual(output, "I am a function.\n")

    def test_whocalled(self):
        with mock.patch.object(sys.modules["__main__"], "__file__", str(FAKE_SCRIPT), create=True):
            output = capture_output(example_project.whocalled)
        lines = output.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "I was imported by fake_script.py")
        self.assertEqual(lines[1], f"I am located in {FAKE_SCRIPT.resolve().parent}")
        self.assertEqual(lines[2], f"My current working directory is {Path.cwd()}")

    def test_message_printed_on_import(self):
        # Reloading re-runs the module's top-level code, just like the first import does
        output = capture_output(importlib.reload, main_module)
        self.assertEqual(output, "This should always appear.\n")



if __name__ == "__main__":
    unittest.main()

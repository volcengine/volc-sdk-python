# coding=utf-8
"""Documentation example execution and supported Python metadata.

Ensures the README get_stats() example runs offline on the current interpreter
(and, via the test suite, on Python 3.7) and that setup.py declares >=3.7.
"""
from __future__ import absolute_import

import os
import unittest


class ExampleRunsTest(unittest.TestCase):
    def test_get_stats_example_main_runs(self):
        # Import and run the example's main() in-process (offline).
        from volcengine.tls.example import get_stats_example
        # Should complete without raising and without network.
        get_stats_example.main()


class SetupMetadataTest(unittest.TestCase):
    def test_python_requires_declares_37(self):
        here = os.path.dirname(os.path.abspath(__file__))
        # repo root is .../volc-sdk-python; setup.py lives there
        root = os.path.abspath(os.path.join(here, "..", "..", ".."))
        setup_path = os.path.join(root, "setup.py")
        if not os.path.exists(setup_path):
            self.skipTest("setup.py not found at expected path")
        with open(setup_path, "r") as fh:
            content = fh.read()
        self.assertIn("python_requires", content)
        self.assertIn("3.7", content)


class ReadmeMentionsGetStatsTest(unittest.TestCase):
    def test_readme_documents_get_stats(self):
        here = os.path.dirname(os.path.abspath(__file__))
        readme = os.path.abspath(os.path.join(here, "..", "README.md"))
        if not os.path.exists(readme):
            self.skipTest("tls README.md not found")
        with open(readme, "r") as fh:
            content = fh.read()
        self.assertIn("get_stats", content)
        self.assertIn("metrics_level", content)
        self.assertIn("StatsOptions", content)
        self.assertIn("set_metrics_level", content)
        self.assertIn("DeltaAdapter", content)


if __name__ == "__main__":
    unittest.main()

import os
import tempfile
import unittest

from volcengine.tls.test import sign_dump


class SignDumpPortabilityTest(unittest.TestCase):
    def test_resolves_fixture_by_walking_up_from_nested_checkout(self):
        with tempfile.TemporaryDirectory() as root:
            fixture = os.path.join(
                root,
                "cospec/changes/check-tls-sdk-contract-alignment/context/l4-snapshots/fixture.json",
            )
            os.makedirs(os.path.dirname(fixture))
            with open(fixture, "w") as f:
                f.write("{}")

            nested = os.path.join(root, "repos/volc-sdk-python")
            os.makedirs(nested)

            self.assertEqual(fixture, sign_dump.resolve_fixture_path(start_dir=nested))

    def test_explicit_fixture_path_wins(self):
        with tempfile.NamedTemporaryFile() as fixture:
            self.assertEqual(fixture.name, sign_dump.resolve_fixture_path(fixture_path=fixture.name))

    def test_output_defaults_to_temp_directory(self):
        old = os.environ.pop("SIGN_OUT_DIR", None)
        try:
            out_path = sign_dump.resolve_output_path()
        finally:
            if old is not None:
                os.environ["SIGN_OUT_DIR"] = old

        self.assertEqual("sign-python.txt", os.path.basename(out_path))
        self.assertTrue(os.path.isdir(os.path.dirname(out_path)))


if __name__ == "__main__":
    unittest.main()

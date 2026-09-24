"""Bounds for the frozen E041 phase-2 rehearsal."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify_e041_phase2.py"
spec = importlib.util.spec_from_file_location("verify_e041_phase2", SCRIPT)
verification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verification)


class Phase2Guards(unittest.TestCase):
    def test_roles_require_train_dev_visible_and_test_hidden(self):
        verification.require_phase2_roles({"TRAIN", "DEV"}, "TEST")
        with self.assertRaises(AssertionError):
            verification.require_phase2_roles({"TRAIN"}, "DEV")

    def test_complete_requires_all_three(self):
        verification.require_complete({name: {} for name in verification.NAMES})
        with self.assertRaises(AssertionError):
            verification.require_complete({"unicef": {}})

    def test_exact_raw_parity_checks_every_vector(self):
        verification.require_exact_parity([[0.2, 0.8], [1.0]], [[0.2, 0.8], [1.0]])
        with self.assertRaises(AssertionError):
            verification.require_exact_parity([[0.2, 0.8], [1.0]], [[0.2, 0.8], [0.9]])
        with self.assertRaises(AssertionError):
            verification.require_exact_parity([[1.0]], [[1.0], [1.0]])

    def test_frozen_hash_and_output_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file"
            path.write_bytes(b"frozen")
            with self.assertRaises(AssertionError):
                verification.require_hash(path, "0" * 64)
            verification.write_new(path.parent / "new", b"one")
            with self.assertRaises(FileExistsError):
                verification.write_new(path.parent / "new", b"two")

    def test_run_preflight_rejects_existing_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            detail = Path(directory) / "detail"
            output.mkdir()
            detail.mkdir()
            verification.require_fresh_outputs(output, detail)
            (detail / "E025-unicef-source.json").write_text("old")
            with self.assertRaises(FileExistsError):
                verification.require_fresh_outputs(output, detail)


if __name__ == "__main__":
    unittest.main()

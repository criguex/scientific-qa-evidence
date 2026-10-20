import tempfile
import unittest
from pathlib import Path

from sanitize_comparator_logs import sanitize


class ComparatorSanitizerTests(unittest.TestCase):
    def test_preserves_acceptance_and_redacts_terminal_private_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "raw.typescript"
            destination = root / "safe.log"
            source.write_text(
                "Script started on 2026-10-20 [COMMAND=cd /Users/cris/work && tool --ip 100.75.2.3]\n"
                "\x1b[32mYour solution is okay!\x1b[0m\n"
                "COMMAND_EXIT_CODE=0\n"
                "peer 100.75.2.3\n"
                "workspace /home/alice/private/project\n",
                encoding="utf-8",
            )

            sanitize(source, destination)

            result = destination.read_text(encoding="utf-8")
            self.assertIn("[COMMAND=<redacted>]", result)
            self.assertIn("Your solution is okay!", result)
            self.assertIn("COMMAND_EXIT_CODE=0", result)
            self.assertIn("<PRIVATE_PATH>", result)
            self.assertIn("<PRIVATE_IP>", result)
            self.assertNotIn("\x1b", result)
            self.assertNotIn("/Users/cris", result)
            self.assertNotIn("/home/alice", result)
            self.assertNotIn("100.75.2.3", result)


if __name__ == "__main__":
    unittest.main()

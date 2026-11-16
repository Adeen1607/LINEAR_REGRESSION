"""Offline regression tests for saved notebook figure extraction."""
import ast
import base64
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_research_site.py"


def load_extractor():
    # Only compile the extractor so these tests need no notebook-rendering dependencies.
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "extract_figs")
    module = ast.fix_missing_locations(ast.Module(body=[func], type_ignores=[]))
    namespace = {"json": json, "base64": base64, "hashlib": hashlib, "re": re}
    exec(compile(module, str(SCRIPT), "exec"), namespace)
    return namespace["extract_figs"]


class FigureExtractionTests(unittest.TestCase):
    def test_same_named_notebooks_do_not_overwrite_figures(self):
        extract_figs = load_extractor()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repository"
            site = repo / "research"
            for folder, payload in [("first", b"image-one"), ("second", b"image-two")]:
                notebook = repo / folder / "analysis.ipynb"
                notebook.parent.mkdir(parents=True)
                notebook.write_text(json.dumps({"cells": [{
                    "cell_type": "code", "metadata": {},
                    "outputs": [{"data": {"image/png": base64.b64encode(payload).decode("ascii")}}]
                }]}), encoding="utf-8")
            figures = extract_figs(repo, site)
            self.assertEqual(len(figures), 2)
            self.assertEqual(len({path.name for path, _ in figures}), 2)
            self.assertEqual({path.read_bytes() for path, _ in figures}, {b"image-one", b"image-two"})
            self.assertEqual([path.name for path, _ in extract_figs(repo, site)], [path.name for path, _ in figures])


if __name__ == "__main__":
    unittest.main()

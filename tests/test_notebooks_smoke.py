"""Smoke tests for executing a subset of tutorial notebooks."""
from __future__ import annotations

import copy
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = REPO_ROOT / "notebooks"

# A representative subset of notebooks that exercise both introductory content
# and plotting workflows. Additional notebooks can be added as coverage needs
# grow.
SMOKE_NOTEBOOKS = (
    NOTEBOOK_DIR / "01_introduction_and_loading_data.ipynb",
    NOTEBOOK_DIR / "03_visualization.ipynb",
)

# Cells that install dependencies or perform other environment mutations can
# dramatically slow down or destabilise CI. We filter them out before executing
# the notebook copy used for testing.
SKIP_CELL_KEYWORDS = ("%pip install", "pip install", "!pip install")


def _to_source_str(source: object) -> str:
    if isinstance(source, str):
        return source
    if isinstance(source, list):
        return "".join(source)
    return ""


def _contains_skip_keyword(source: object) -> bool:
    text = _to_source_str(source)
    return any(keyword in text for keyword in SKIP_CELL_KEYWORDS)


@pytest.mark.parametrize("notebook_path", SMOKE_NOTEBOOKS)
def test_notebook_executes(notebook_path: Path) -> None:
    """Execute a notebook end-to-end with nbclient."""
    if not notebook_path.exists():
        pytest.skip(f"Notebook {notebook_path} not present")

    nb = nbformat.read(notebook_path, as_version=4)
    sanitized_nb = copy.deepcopy(nb)
    sanitized_nb.cells = [
        cell
        for cell in sanitized_nb.cells
        if not (
            cell.get("cell_type") == "code"
            and _contains_skip_keyword(cell.get("source"))
        )
    ]

    client = NotebookClient(
        sanitized_nb,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": notebook_path.parent}},
    )
    client.execute()

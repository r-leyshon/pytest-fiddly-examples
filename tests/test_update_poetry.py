"""Tests for update_poetry module."""
import os

from example_pkg import update_poetry

def test_update_poem_writes_new_pattern_to_file(tmp_path):
    """Check that update_poem changes the poem pattern and writes to file."""
    new_poem_path = os.path.join(tmp_path, "new_poem.txt")
    update_poetry.update_poem(
        poem_pth="tests/data/jack-jill-2024.txt",
        target_pattern="glitch",
        replacement="bug",
        out_file=new_poem_path
        )
    assert os.path.exists(new_poem_path)
    # let's check what pattern was written
    with open(new_poem_path, "r") as f:
        what_was_written = f.read()
        f.close()
    assert "glitch" not in what_was_written
    assert "bug" in what_was_written
    assert os.listdir(tmp_path) == ["new_poem.txt"]


def test_do_i_get_a_new_tmp_path(tmp_path):
    """Remind ourselves that tmp_path is function-scoped."""
    assert "new_poem" not in os.listdir(tmp_path)
    assert os.listdir(tmp_path) == []

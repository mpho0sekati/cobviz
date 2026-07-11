import pytest
from pathlib import Path
import tempfile
import shutil
import os
from cobviz.repository import find_cobol_files, clone_repo
from unittest.mock import patch, MagicMock
import git

def test_find_cobol_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Create some dummy files
        (tmp_path / "test.cob").touch()
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "other.cbl").touch()
        (tmp_path / "not_cobol.txt").touch()
        (tmp_path / "another.COBOL").touch()

        files = find_cobol_files(tmpdir)

        # Should find 3 files
        assert len(files) == 3
        assert Path("another.COBOL") in files
        assert Path("test.cob") in files
        assert Path("subdir/other.cbl") in files
        assert Path("not_cobol.txt") not in files

@patch("git.Repo.clone_from")
def test_clone_repo_success(mock_clone):
    mock_clone.return_value = MagicMock()
    url = "https://github.com/example/repo.git"
    dest = "/tmp/fake-repo"

    result = clone_repo(url, dest)

    assert result == dest
    mock_clone.assert_called_once_with(url, dest, depth=1)

@patch("git.Repo.clone_from")
def test_clone_repo_failure(mock_clone):
    mock_clone.side_effect = git.GitCommandError("clone", "error")
    url = "https://github.com/example/repo.git"
    dest = "/tmp/fake-repo"

    with pytest.raises(RuntimeError) as excinfo:
        clone_repo(url, dest)

    assert "Failed to clone repository" in str(excinfo.value)

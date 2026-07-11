import os
from pathlib import Path
import git
import logging

logger = logging.getLogger(__name__)

def clone_repo(url: str, dest_dir: str) -> str:
    """
    Clones a git repository to the specified destination directory.
    Uses depth=1 for a shallow clone to save time and space.
    """
    try:
        logger.info(f"Cloning repository {url} to {dest_dir}")
        git.Repo.clone_from(url, dest_dir, depth=1)
        return dest_dir
    except git.GitCommandError as e:
        logger.error(f"Git clone error: {str(e)}")
        raise RuntimeError(f"Failed to clone repository: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during clone: {str(e)}")
        raise RuntimeError(f"An unexpected error occurred during cloning: {str(e)}")

def find_cobol_files(directory: str) -> list[Path]:
    """
    Recursively finds all COBOL files in a directory.
    Returns a list of Path objects relative to the provided directory.
    """
    cobol_extensions = {'.cob', '.cbl', '.cpy', '.coo', '.ccp', '.cobol'}
    base_path = Path(directory)
    cobol_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in cobol_extensions:
                try:
                    cobol_files.append(file_path.relative_to(base_path))
                except ValueError:
                    # In case of weird path issues
                    continue

    return sorted(cobol_files)

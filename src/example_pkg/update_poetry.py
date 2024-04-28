"""Demonstrating tmp_path & tmp_path_factory with a simple txt file."""
from pathlib import Path
from typing import Union

def _update_a_term(
    txt_pth: Union[Path, str], target_pattern:str, replacement:str) -> str:
    """Replace the target pattern in a body of text.

    Parameters
    ----------
    txt_pth : Union[Path, str]
        Path to a txt file.
    target_pattern : str
        The pattern to replace.
    replacement : str
        The replacement value.

    Returns
    -------
    str
        String with any occurences of target_pattern replaced with specified
        replacement value.

    """
    with open(txt_pth, "r") as f:
        txt = f.read()
        f.close()
    return txt.replace(target_pattern, replacement)


def _write_string_to_txt(some_txt:str, out_pth:Union[Path, str]) -> None:
    """Write some string to a text file.

    Parameters
    ----------
    some_txt : str
        The test to write to file.
    out_pth : Union[Path, str]
        The path to the file.
    
    Returns
    -------
    None

    """
    with open(out_pth, "w") as f:
        f.writelines(some_txt)
        f.close()    


def update_poem(
    poem_pth:Union[Path, str],
    target_pattern:str,
    replacement:str,
    out_file:Union[Path, str]) -> None:
    """Takes a txt file, replaces a pattern and writes to a new file.

    Parameters
    ----------
    poem_pth : Union[Path, str]
        Path to a txt file.
    target_pattern : str
        A pattern to update.
    replacement : str
        The replacemetn value.
    out_file : Union[Path, str]
        A file path to write to.

    """
    txt = _update_a_term(poem_pth, target_pattern, replacement)
    _write_string_to_txt(txt, out_file)

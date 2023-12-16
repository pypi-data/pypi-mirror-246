from typing import Any
import json
import re


def parse_misparsed(text: str, open: str = None, close: str = None, normalize_newline: bool = True, to_json: bool = True) -> Any:
    """Parse misparsed JSON.
    Args:
        text (str): The text to parse.
        open (str, optional): The open character. Defaults to None.
        close (str, optional): The close character. Defaults to None.
    Returns:
        JSON: The parsed JSON.
    """
    if open is None:
        open = '{"'
    if close is None:
        close = ']}'


    # Remove the extra spaces around the start and end of the JSON.
    # This is necessary for the JSON to be parsed correctly.
    pattern: str = None

    if open.startswith('{'):
        pattern = r'(?<=\{)\s+|\s+(?=\})'
    elif open.startswith('['):
        pattern = r'(?<=\[)\s+|\s+(?=\])'

    if pattern:
        text = re.sub(pattern, '', text)

    try:
        start = text.index(open)
        end = text.rindex(close) + len(close)
        text = text[start:end]
    except ValueError:
        text = text

    if normalize_newline:
        text = text.replace('\\n', '\n').replace("\n", "\\n")

    if to_json:
        return json.loads(text)
    else:
        return text

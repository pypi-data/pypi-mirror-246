import json
from pathlib import Path

import pytest

from twlib.environment import ROOT_DIR
from twlib.lib.osdir.path import scan_directory
from twlib.lib.string.chunking import (
    parse_markdown_to_html,
    remove_code_blocks,
    remove_excessive_dots,
    split_into_chunks_with_tiktoken,
)


def test_remove_excessive_dots():
    # Example usage
    original_text = (
        "This is a test.... with more than four dots..... and here's another...."
    )
    cleaned_text = remove_excessive_dots(original_text)
    assert cleaned_text == "This is a test with more than four dots and here's another"


def test_split_into_chunks():
    p = ROOT_DIR / "tests/resources/md/r1.md"
    html_content = parse_markdown_to_html(p)
    text_without_code = remove_code_blocks(html_content)
    chunks = split_into_chunks_with_tiktoken(text_without_code, max_chunk_size=20)
    assert len(chunks) == 16


@pytest.mark.skip("experimentation")
def test_xxx():
    directory = Path("/Users/Q187392/dev/s/private/vimwiki")
    md_files = scan_directory(directory)

    for md_file in md_files:
        html_content = parse_markdown_to_html(directory / md_file)
        text_without_code = remove_code_blocks(html_content)
        chunks = split_into_chunks_with_tiktoken(text_without_code, max_chunk_size=20)

        for i, chunk in enumerate(chunks):
            id_ = str(md_file) + f":{i}"

            json_output = json.dumps({"id": id_, "content": chunk})
            print(json_output)

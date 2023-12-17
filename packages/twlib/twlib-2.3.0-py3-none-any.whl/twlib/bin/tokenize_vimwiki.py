import json
from pathlib import Path

from twlib.lib.osdir.path import scan_directory
from twlib.lib.string.chunking import (
    parse_markdown_to_html,
    remove_code_blocks,
    split_into_chunks_with_tiktoken,
)

"""
jina-embeddings-v2-small-en is an English, monolingual embedding model supporting 8192 sequence length. It is based on a Bert architecture
 text-embedding-ada-002 model: 8191
"""


def main():
    directory = Path("/Users/Q187392/dev/s/private/vimwiki")
    md_files = scan_directory(directory)

    for md_file in md_files:
        if md_file.is_symlink():
            continue
        html_content = parse_markdown_to_html(directory / md_file)
        text_without_code = remove_code_blocks(html_content)
        chunks = split_into_chunks_with_tiktoken(text_without_code, max_chunk_size=8191)
        # chunks = split_into_chunks_with_tokenizer(text_without_code, max_tokens=8191)

        for i, chunk in enumerate(chunks):
            id_ = str(md_file) + f":{i}"

            json_output = json.dumps({"id": id_, "content": chunk})
            print(json_output)


if __name__ == "__main__":
    main()

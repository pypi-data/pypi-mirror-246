import re
from pathlib import Path

import markdown2
import tiktoken
from bs4 import BeautifulSoup
from transformers import AutoTokenizer


def remove_excessive_dots(text):
    pattern = r"\.{4,}"
    # Change '' to '.' if you want to replace with a single dot instead of removing
    return "\n".join(re.sub(pattern, "", text) for text in text.split("\n"))


def strip_quote_prefixes(text):
    return "\n".join(
        line[2:] if line.startswith("> ") else line for line in text.split("\n")
    )


def parse_markdown_to_html(file_path: Path) -> markdown2.UnicodeWithAttrs:
    md_content = file_path.read_text(encoding="utf-8", errors="ignore")
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     md_content = file.read()
    md_content = strip_quote_prefixes(md_content)
    md_content = remove_excessive_dots(md_content)
    # return markdown.markdown(md_content)
    return markdown2.markdown(md_content, extras=["fenced-code-blocks"])


def remove_code_blocks(html_content: markdown2.UnicodeWithAttrs) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for code_block in soup.find_all(["code", "pre"]):
        code_block.decompose()
    return soup.get_text(strip=True, separator="\n")


def split_into_chunks_with_tiktoken(text, max_chunk_size=2048) -> list[str]:
    """tiktoken models:
    cl100k_base	gpt-4, gpt-3.5-turbo, text-embedding-ada-002
    p50k_base	Codex models, text-davinci-002, text-davinci-003
    r50k_base (or gpt2)	GPT-3 models like davinci
    """
    # Implement logic to split text into chunks based on paragraphs, headers, etc.
    # This is a simplified example that splits based on character count
    chunks = []
    current_chunk = []
    current_length = 0
    encoding = tiktoken.get_encoding("cl100k_base")
    # encodings = encoding.encode(text)

    for word in text.split():
        word_tokens = encoding.encode(word)
        word_token_length = len(word_tokens)

        if current_length + word_token_length > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_token_length
        else:
            current_chunk.append(word)
            current_length += word_token_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))  # Add the last chunk if not empty

    return chunks


def split_into_chunks_with_tokenizer(text, max_tokens=8191) -> list[str]:
    """Split text into chunks with a maximum token count."""
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokens = tokenizer.tokenize(text)
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(current_chunk) + 1 <= max_tokens:
            current_chunk.append(token)
        else:
            chunks.append(tokenizer.convert_tokens_to_string(current_chunk))
            current_chunk = [token]

    if current_chunk:
        chunks.append(tokenizer.convert_tokens_to_string(current_chunk))

    return chunks

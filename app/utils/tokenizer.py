import tiktoken
from typing import List

# This encoding is a good general-purpose choice for modern models and multiple languages.
enc = tiktoken.get_encoding("cl100k_base")

def chunk_text_by_tokens(text: str, tokens_per_chunk: int) -> List[str]:
    """
    Splits a text string into a list of smaller strings, with each chunk
    containing approximately the specified number of tokens.

    Args:
        text: The input text to be split.
        tokens_per_chunk: The target number of tokens for each chunk.

    Returns:
        A list of text chunks.
    """
    if not text or tokens_per_chunk <= 0:
        return []

    # Encode the entire text into a list of token integers
    tokens = enc.encode(text)
    
    chunks = []
    # Iterate through the token list, creating slices of the desired size
    for i in range(0, len(tokens), tokens_per_chunk):
        chunk_tokens = tokens[i:i + tokens_per_chunk]
        # Decode the token slice back into a readable string
        chunks.append(enc.decode(chunk_tokens))
        
    return chunks
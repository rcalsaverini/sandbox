from typing import Callable
from pathlib import Path
from itertools import zip_longest
from openai import OpenAI
import textwrap
from config import settings

PATH = Path("/mnt/c/Users/user/Downloads/kapital.md")
Oracle = Callable[[str], list[str]]
client = OpenAI(
    api_key=settings.keys.openai,
)


def splitter(words, num_chunks):
    iterators = [iter(words)] * num_chunks
    return [
        list(filter(None, item)) for item in zip_longest(*iterators, fillvalue=None)
    ]


def tree_search(
    oracle: Oracle, string: str, min_size: int, num_chunks: int
) -> list[str]:
    stack = [string.split()]
    output = []
    while stack:
        words = stack.pop()
        if len(words) > min_size:
            chunks = splitter(words, num_chunks)
            print(len(chunks), list(map(len, chunks)))
            filtered_chunks = oracle(chunks)
            stack.extend(filtered_chunks)
        else:
            output.append(" ".join(words))
    return output


def gpt_oracle(question: str) -> Oracle:
    def oracle(chunks: list[str]) -> list[str]:
        system_prompt = textwrap.dedent("""\
        You are an expert document navigator. Your task is to:
        1. Identify which text chunks might contain information to answer the user's question
        2. Record your reasoning in a scratchpad for later reference
        3. Choose chunks that are most likely relevant. Be selective, but thorough. Choose as many chunks as you need to answer the question, but avoid selecting too many.

        First think carefully about what information would help answer the question, then evaluate each chunk.
        """)

        user_message = f"QUESTION: {question}\n\nTEXT CHUNKS:"
        for k, chunk in enumerate(chunks):
            user_message += f"CHUNK {k}\n{chunk}\n\n"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        response = client.responses.create(model="gpt-4.1-nano", input=messages)

        return response

    return oracle


if __name__ == "__main__":
    text = PATH.read_text()
    chunks = [" ".join(chunk) for chunk in splitter(text.split(), 25)]

    response = gpt_oracle("what is the definition of surplus-value?")(chunks)
    import ipdb

    ipdb.set_trace()

    # def has_commas(strings: list[str]) -> list[str]:
    #     return [string for string in strings if "surplus-value" in string]

    # output = tree_search(has_commas, PATH.read_text(), min_size=25, num_chunks=10)
    # for k, line in enumerate(output):
    #     print(k, line)
    #     pass

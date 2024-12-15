import os
import pytest

from reiai import text_process
from reiai import gpt_base


def test_extract_addresses():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = gpt_base.get_openai_client(openai_api_key)
    model = "gpt-4o-mini"
    text = open("tests/data/text_with_addresses.txt").read()
    addresses, usage = text_process.extract_addresses(text, client, model, n_words=1000, repeat=2)
    # check addresses extracted
    assert len(addresses) > 0






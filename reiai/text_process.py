"""
Module Name: text_process
Description: gpt API for processing real estate related texts

Author: Masaru Nakajima

Copyright (c) 2024 Masaru Nakajima
"""


import pypdf
from tqdm import tqdm
import warnings
import pandas as pd

from . import gpt_base
from . import gmap


def extract_addresses_unit(text, client, model, params={}):
    """
    Given a text, return the addresses extracted from the text.
    :param text: Text to process
    :param client: OpenAI API client
    :param model: GPT model
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    """

    system_prompt = """
    You are a helpful assistant for a real estate investor. 
    You are given a text that contains addresses. 
    You need to extract the property addresses from the text.
    Make sure to extract the exact string that represents the address.
    If you detect partial address, include extactly the partial address 
    and don't try to complete the address.
    The output should be in json format without any other text before 
    or after the json object.
    Example output would be:
    """
    system_prompt += """
    {
        "addresses": [
            "123 Main St, San Francisco, CA 94105",
            "456 Elm St",
            "789 Oak St, Apt 101",
            "101 Pine St"
        ]
    }
    """

    prompt = text
    params["response_format"] = {"type": "json_object"}

    response = gpt_base.chat_completion_simple(
        client, model, system_prompt, prompt, params
    )
    json_data, usage = gpt_base.parse_gpt_chat_response_json(response)
    addresses = json_data.get("addresses", [])

    return addresses, usage


def extract_addresses(text, client, model, params={}, n_words=1000, repeat=1):
    """
    Given a text, return the addresses extracted from the text.
    :param text: Text to process
    :param client: OpenAI API client
    :param model: GPT model
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    """

    text_batches = []
    n_overlap_words = 10
    words = text.split()
    n_words_total = len(words)
    n_batches = n_words_total // (n_words - n_overlap_words) + 1
    for i in range(n_batches):
        start = i * (n_words - n_overlap_words)
        end = min(start + n_words, n_words_total)
        text_batch = " ".join(words[start:end])
        for _ in range(repeat):
            text_batches.append(text_batch)

    addresses = []
    prompt_tokens = 0
    completion_tokens = 0
    for text_batch in text_batches:
        addresses_batch, usage = extract_addresses_unit(
            text_batch, client, model, params
        )
        addresses.extend(addresses_batch)
        prompt_tokens += usage.prompt_tokens
        completion_tokens += usage.completion_tokens

    # make everything upper case
    addresses = [address.upper() for address in addresses]
    addresses = list(set(addresses))

    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
    }
    return addresses, usage


def extract_addresses_pdf(
    pdf_path, client, model, params={}, n_words=1000, repeat=1
):
    """
    Extract addresses from pdf file.
    :param pdf_path: path to pdf_file
    :param client: OpenAI API client
    :param model: GPT model
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    """

    reader = pypdf.PdfReader(pdf_path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text())
    text = " ".join(texts)
    return extract_addresses(
        text, client, model, params, n_words=n_words, repeat=repeat
    )


def lookup_address(addresses, api_key):
    """
    Given a list of address strings, return the geocoded addresses.
    :param addresses: List of address strings
    :param api_key: Google Map API key
    :return: dataframe of geocoded addresses
    """

    if addresses is None or len(addresses) == 0:
        return pd.DataFrame()
    address_df = pd.DataFrame()
    for address in tqdm(addresses):
        data = gmap.geocode(address, api_key)
        address_df = pd.concat([address_df, pd.DataFrame([data])], ignore_index=True)
    
    # remove duplicate full addresses
    address_df = address_df.drop_duplicates(subset=["full_address"])
    address_df = address_df.reset_index(drop=True)

    return address_df

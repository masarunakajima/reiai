"""
Module Name: text_process
Description: gpt API for processing real estate related texts

Author: Masaru Nakajima

Copyright (c) 2024 Masaru Nakajima
"""


import gpt_base


def extract_addresses(text, client, model, params={}):
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
    params["response_format"] = "json"

    return gpt_base.chat_completion_simple(
        client, model, system_prompt, prompt, params
    )

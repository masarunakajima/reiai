"""
Module Name: gpt_base
Description: Basic GPT API calls

Author: Masaru Nakajima

Copyright (c) 2024 Masaru Nakajima
"""

import os
from openai import OpenAI
import warnings
import json

# import BadRequestError from openai module

from openai import BadRequestError


def get_openai_client(openai_api_key):
    """
    Create an OpenAI API client
    :param openai_api_key: API key for OpenAI
    :return: OpenAI API client
    """

    return OpenAI(api_key=openai_api_key)


def chat_completion(client, model, messages, params):
    """
    Given a prompt, return the completion from the GPT model.
    :param client: OpenAI API client
    :param model: GPT model
    :param messages: List of messages (list of dictionaries with 'role' and 'content' keys)
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    :return: response from the GPT chat API
    """

    query_dict = {
        "model": model,
        "messages": messages,
    }
    query_dict.update(params)
    try:
        response = client.chat.completions.create(**query_dict)
    except BadRequestError as e:
        # show warning
        warnings.warn(f"Bad request error: {e}")
        return None
    return response


def gpt_chat_test(client, model):
    """
    Test the GPT chat API
    :param client: OpenAI API client
    :param model: GPT model
    :return: response from the GPT chat API
    """

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for a real estate investor.",
        },
        {"role": "user", "content": "Ok?"},
    ]
    return chat_completion(client, model, messages, {})


def parse_gpt_chat_response_json(response):
    """
    Parse the JSON response from the GPT chat API
    :param response: JSON response from the GPT chat API
    :return: json_response, usage
    """

    if response is None:
        return None, None

    usage = response.usage
    # Get the chat completion
    completion = response.choices[0].message.content

    json_response = json.loads(completion)

    return json_response, usage


def chat_completion_simple(client, model, system_prompt, prompt, params):
    """
    Given a system prompt and a user prompt, return the completion from the GPT model.
    :param client: OpenAI API client
    :param model: GPT model
    :param system_prompt: System prompt (e.g. "You are a real estate agent.")
    :param prompt: User prompt (e.g. "What is the address of the property?")
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    :return: response from the GPT chat API
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    return chat_completion(client, model, messages, params)

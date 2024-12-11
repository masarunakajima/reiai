"""
Module Name: gpt_base
Description: Basic GPT API calls

Author: Masaru Nakajima

Copyright (c) 2024 Masaru Nakajima
"""

import os
from openai import OpenAI


def get_openai_client(openai_api_key):
    """
    Create an OpenAI API client
    :param openai_api_key: API key for OpenAI
    """
    return OpenAI(openai_api_key)


def chat_completion(client, model, messages, params):
    """
    Given a prompt, return the completion from the GPT model.
    :param client: OpenAI API client
    :param model: GPT model
    :param messages: List of messages (list of dictionaries with 'role' and 'content' keys)
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    """

    query_dict = {
        "model": model,
        "messages": messages,
    }
    query_dict.update(params)
    response = client.chat.completions.create(**query_dict)
    return response


def chat_completion_simple(client, model, system_prompt, prompt, params):
    """
    Given a system prompt and a user prompt, return the completion from the GPT model.
    :param client: OpenAI API client
    :param model: GPT model
    :param system_prompt: System prompt (e.g. "You are a real estate agent.")
    :param prompt: User prompt (e.g. "What is the address of the property?")
    :param params: Dictionary of parameters (e.g. max_tokens, temperature)
    """

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    return chat_completion(client, model, messages, params)
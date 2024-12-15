import click
import os
import json
import pandas as pd

from . import gpt_base
from . import text_process


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pdf_path")
@click.argument("output_path")
@click.option("--n_words", default=1000, help="Number of words per batch")
@click.option(
    "--repeat", default=1, help="Number of times to repeat each batch"
)
@click.option("--openai_api_key", help="OpenAI API key")
def extract_addresses_pdf(
    pdf_path, output_path, n_words, repeat, openai_api_key
):
    """
    Extract addresses from pdf file.
    :param pdf_path: path to pdf_file
    :param output_path: path to output file
    :param n_words: Number of words per batch
    :param repeat: Number of times to repeat each batch
    :param openai_api_key: OpenAI API key
    """

    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        raise ValueError(
            "Make sure to either set the OPENAI_API_KEY environment variable or pass it as an argument"
        )

    client = gpt_base.get_openai_client(openai_api_key)
    model = "gpt-4o-mini"
    addresses, usage = text_process.extract_addresses_pdf(
        pdf_path, client, model, n_words=n_words, repeat=repeat
    )
    output_json = {"addresses": addresses}
    output_json.update(usage)
    with open(output_path, "w") as f:
        json.dump(output_json, f)


@cli.command()
@click.argument("input_path")
@click.argument("output_path")
@click.argument("extra_strings", nargs=-1)
@click.option("--api-key", help="Google Map API key")
def geocode_lookup(input_path, output_path, extra_strings, api_key):
    """
    Given a list of address strings, return the geocoded addresses.
    :param input_path: path to input json file with key "addresses"
    :param output_path: path to output file
    :param extra_strings: Extra address strings
    :param api_key: Google Map API key
    """

    if api_key is None:
        api_key = os.getenv("GOOGLE_MAP_API_KEY")
        if api_key is None:
            raise ValueError(
                "Make sure to either set the GOOGLE_MAP_API_KEY environment variable or pass it as an argument"
            )

    with open(input_path, "r") as f:
        data = json.load(f)
    if "addresses" not in data:
        raise ValueError("Input json file must have key 'addresses'")
    addresses = data["addresses"]
    addresses = [address + ", " + ", ".join(extra_strings) for address in addresses]
    addresses = text_process.lookup_address(addresses, api_key)
    addresses.to_csv(output_path, index=False)

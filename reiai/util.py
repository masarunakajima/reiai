import pandas as pd

def split_address(address: str) -> list[str]:
    """
    Split address into parts. It splits by comma and assumes
    that the third part is state and zipcode.
    :param address: address string
    :return: list of address parts
    """
    split = address.strip().split(",")
    if len(split) < 3:
        return split
    address_list = split[:2]
    address_list = split[2].split()
    if len(split) > 3:
        address_list.extend(split[3:])
    return address_list


def get_unique_vals(df: pd.DataFrame, max_vals: int = 10) -> dict:
    """
    Get unique values for each column in the dataframe.
    :param df: dataframe
    :param max_vals: maximum number of unique values to return
    :return: dictionary of unique values
    """
    unique_vals = {}
    for col in df.columns:
        vals = df[col].unique()
        if len(vals) > max_vals:
            vals = vals[:max_vals]
        unique_vals[col] = vals
    return unique_vals




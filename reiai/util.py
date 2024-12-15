def split_address(address: str) -> List[str]:
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

# ai suggested code
def sort_dicts_by_key(dicts, key, reverse=False):
    """AI-style suggested implementation: simple, concise, uses Python's sorted with a lambda.

    Args:
        dicts (list[dict]): list of dictionaries
        key (str): key to sort by
        reverse (bool): descending if True
    """
    return sorted(dicts, key=lambda d: d.get(key, None), reverse=reverse)


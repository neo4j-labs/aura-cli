"""This module defines functions for formatting the CLI output"""


def format_table_output(data: dict):
    """
    Function to format the data in a dictionary into a table.
    """
    if not data or isinstance(data, str):
        return data

    # Make sure data is a list
    if isinstance(data, dict):
        data = [data]

    headers = data[0].keys()
    rows = [[str(val) for val in list(d.values())] for d in data]

    # Find max length in each column
    col_widths = [max(len(str(x)) for x in col) for col in zip(*([headers] + rows))]

    # Create a format specifier for each column width
    format_spec = " | ".join(["{{:{}}}".format(w) for w in col_widths])

    res = format_spec.format(*headers) + "\n"
    res += "-" * len(format_spec.format(*headers))
    for row in rows:
        res += "\n" + format_spec.format(*row)

    return res


def format_text_output(data: dict):
    """
    Function to format the data in a dictionary into lines of tab-seperated text.
    """
    if not data or isinstance(data, str):
        return data

    # Make sure data is a list
    if isinstance(data, dict):
        data = [data]

    headers = data[0].keys()
    rows = [[str(val) for val in list(d.values())] for d in data]

    # Find max length in each column
    col_widths = [max(len(str(x)) for x in col) for col in zip(*([headers] + rows))]

    # Create a format specifier for each column width
    format_spec = " \t ".join(["{{:{}}}".format(w) for w in col_widths])

    res = format_spec.format(*headers)
    for row in rows:
        res += "\n" + format_spec.format(*row)

    return res

def format_table_output(data, printing=True):
    if not data:
        return print("")
    if isinstance(data, str):
        return print(data)

    # Make sure data is a list
    if isinstance(data, dict):
        data = [data]

    headers = data[0].keys()
    rows = [[str(val) for val in list(d.values())] for d in data]

    # Find max length in each column
    col_widths = [max(len(str(x)) for x in col) for col in zip(*([headers] + rows))]

    # Create a format specifier for each column width
    format_spec = " | ".join(["{{:{}}}".format(w) for w in col_widths])

    print(format_spec.format(*headers))
    print("-" * len(format_spec.format(*headers)))
    for row in rows:
        print(format_spec.format(*row))


def format_text_output(data, printing=True):
    if not data:
        return print("")
    if isinstance(data, str):
        return print(data)

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

    if printing:
        print(res)
    else:
        return res

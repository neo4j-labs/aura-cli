def print_table(data):
    if not data:
        return print("")

    headers = data[0].keys()
    rows = [list(d.values()) for d in data]

    # Find max length in each column
    col_widths = [
        max(len(str(x)) for x in col)
        for col in zip(*([headers] + rows))
    ]

    # Create a format specifier for each column width
    format_spec = ' | '.join(['{{:{}}}'.format(w) for w in col_widths])

    print(format_spec.format(*headers))
    print('-' * len(format_spec.format(*headers)))
    for row in rows:
        print(format_spec.format(*row))


def print_text(data):
    if not data:
        return print("")

    headers = data[0].keys()
    rows = [list(d.values()) for d in data]

    # Find max length in each column
    col_widths = [
        max(len(str(x)) for x in col)
        for col in zip(*([headers] + rows))
    ]

    # Create a format specifier for each column width
    format_spec = ' \t '.join(['{{:{}}}'.format(w) for w in col_widths])

    print(format_spec.format(*headers))
    for row in rows:
        print(format_spec.format(*row))


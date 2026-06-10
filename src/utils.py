def row_to_dict(columns, row):
    return dict(zip(columns, row))


def rows_to_dict(columns, rows):
    lista = []

    for row in rows:
        lista.append(row_to_dict(columns, row))

    return lista
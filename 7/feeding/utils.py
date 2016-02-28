def get_or_else(xs, index, default=None):
    """gets value at the index if it is in range, else default

    :param xs: elements to get a value from
    :type xs: list

    :param index: index to check
    :type index: int

    :param default: default value
    :type default: any

    :returns: value at index or default
    :rtype: any
    """

    try:
        return xs[index]
    except IndexError:
        return default

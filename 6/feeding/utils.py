def max_order_preserving(xs):
    """gets the max of a list prefering original ordering in case of ties

    :param xs: elements to get max of
    :type xs: list

    :returns: max
    :rtype: any
    """

    max_value = None

    for x in xs:
        if max_value is None or x > max_value:
            max_value = x

    return max_value


def get_or_else(xs, maybe_index, default=None):
    """gets value at the maybe_index index if it is in range, else default

    :param xs: elements to get a value from
    :type xs: list

    :param maybe_index: index to check
    :type maybe_index: int

    :param default: default value
    :type default: any

    :returns: value at index or default
    :rtype: any
    """

    if 0 <= maybe_index < len(xs):
        return xs[maybe_index]

    return default


def sorted_with_default(xs, default_order):
    """sorts the list settling ties with default_order

    :param xs: list to sort
    :type xs: list of any

    :param default_order: order to default on ties
    :type default_order: list of int

    :returns: sorted list
    :rtype: list of any
    """

    return map(
        lambda x_default: x_default[0],
        sorted(
            zip(xs, reversed(default_order)),
            key=lambda x_default: (x_default[0], x_default[1]),
            reverse=True))

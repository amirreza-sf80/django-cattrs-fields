import decimal


def quantize(value: decimal.Decimal, attrs: dict):
    """
    Quantize the decimal value to the configured precision.
    """
    if attrs["decimal_places"] is None:
        return value

    context = decimal.getcontext().copy()
    if attrs["max_digits"] is not None:
        context.prec = attrs["max_digits"]
    return value.quantize(decimal.Decimal(".1") ** attrs["decimal_places"], context=context)

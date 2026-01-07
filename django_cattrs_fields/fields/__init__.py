import datetime
from decimal import Decimal
import uuid

from attrs import frozen


@frozen
class Params:
    """param class for passing extra data to fields

    Attributes
    ----------
    decimal_max_digits : (for DecimalField only) maximum number of digits allowed in the number.

    decimal_places : (for DecimalField only) the number of decimal places to store with the number.
    """

    decimal_max_digits: int | None = None  # for DecimalField only
    decimal_places: int | None = None  # for DecimalField only


type BooleanField = bool

type CharField = str

type EmailField = str

type SlugField = str

type URLField = str

type UUIDField = uuid.UUID

type IntegerField = int

type DecimalField = Decimal

type FloatField = float

type DateField = datetime.date

type DateTimeField = datetime.datetime

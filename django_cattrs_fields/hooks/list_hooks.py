from typing import TYPE_CHECKING, Any, get_args, get_origin

from attrs import has

from django.db.models import Model
from django.forms.models import model_to_dict

if TYPE_CHECKING:
    from cattrs.converters import Converter

# the issue we are trying to solve here is model objects
# django model objects are not dict like objects,
# but cattrs expects any incoming object to be dict like
# so there are these solutions:
# 1. we call `model_to_dict` on each incoming object
# 2. user adds `__contains__` and `__getitem__` to their models
# 3. user converts model objects to dict before structuring
# option 1 seems more user friendly, but i don't have a clear image which one would be better


def list_structure_hook_factory(cls: Any, converter: "Converter"):
    (elem_type,) = get_args(cls)

    def hook(obj, _):
        return [
            converter.structure(model_to_dict(item) if isinstance(item, Model) else item, elem_type)
            for item in obj
        ]

    return hook


def is_list_of_attrs(tp):
    return get_origin(tp) is list and has(get_args(tp)[0])

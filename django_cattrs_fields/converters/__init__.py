from cattrs.converters import Converter

from django.conf import settings

from .register_hooks import (
    register_all_unstructure_hooks,
    register_structure_hooks,
    register_model_structure_hook,
    register_all_empty_unstructure_hooks,
)

converter = Converter()


register_structure_hooks(converter)
register_all_unstructure_hooks(converter)

# recommended way of using empty hooks is by creating a dedicated converter
if getattr(settings, "DCF_EMPTY_HOOKS", False):
    register_all_empty_unstructure_hooks(converter)


if getattr(settings, "DCF_MODEL_HOOKS", True):
    register_model_structure_hook(converter)

from cattrs.converters import Converter

from .register_hooks import register_unstructure_hooks, register_structure_hooks

converter = Converter()


register_structure_hooks(converter)
register_unstructure_hooks(converter)

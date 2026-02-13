# django-cattrs-fields

[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-cattrs-fields/)

**Note**: this is a very experimental project, I'm mostly navigating and discovering how this could work,
as much as any help and feedback is appreciated, please do not use in a production environment.

Brings [cattrs](https://github.com/python-attrs/cattrs) support to the django world.

this project is the first step of many, it is intended to be minimal, only adding data type support.

### current data types
* BooleanField
* CharField
* DecimalField
* EmailField
* SlugField
* URLField
* UUIDField
* IntegerField
* FloatField
* DateField
* DateTimeField
* FileField
* TimeField
* EmptyField

## installing
this is not packaged to PyPI yet, for using you need to clone the repository first.

then install the package by running `uv sync` or `uv sync --extra <group name>` where group name is one of optional-dependencies listed in pyproject.toml.

if you want a one-shot install use `uv sync --all-extras`



## basic usage:
data model classes are `attrs` classes, so anything you find in [attrs](https://www.attrs.org/en/stable/index.html) docs also applies here.
we also follow cattrs, so anything in their [docs](https://catt.rs/en/stable/index.html) also applies

```py
import uuid
from datetime import date, datetime, time
from decimal import Decimal

from attrs import define

from django.core.files.uploadedfile import SimpleUploadedFile

from django-cattrs-fields.converters import converter
from django_cattrs_fields.fields import (
  BooleanField, 
  CharField, 
  DecimalField,
  EmailField, 
  SlugField, 
  URLField, 
  UUIDField, 
  IntegerField, 
  FloatField, 
  DateField,
  DateTimeField,
  TimeField,
)
from django_cattrs_fields.fields.files import FileField

@define
class Human:
    id: UUIDField
    username: CharField
    email: EmailField
    slug: SlugField
    website: URLField
    age: IntegerField
    salary: FloatField
    birth_date: DateField
    signup_date: DateTimeField
    picture: FileField
    accurate_salary: DecimalField
    lunch_time: TimeField


human = {
    "id": uuid.uuid4(),
    "username": "bob",
    "email": "bob@email.com",
    "slug": "bo-b",
    "website": "https://bob.com",
    "age": 25,
    "salary": 1000.43,
    "birth_date": date(year=2000, month=7, day=3),
    "signup_date": datetime.now(),
    "picture": SimpleUploadedFile(name="test_image.jpeg", content=b"wheeee", content_type="image/jpeg"),
    "accurate_salary": Decimal("1000.43"),
    "lunch_time": time(14, 30, 0),
}

structure = converter.structure(human, Human)  # runs structure hooks and validators, then creates an instance of `Human`
normal_data = converter.unstructure(structure)  # runs unstructure hooks, then makes a dict similar to `human` (or what you tell it to), no validators run.
```

### list and querysets
when we are working with a list of multiple objects or a queryset that would contains multiple objects, we need to tell `structure` and `unstructure` that it's working with a list

```py
@define
class FoodData:
    name: CharField
    rate: IntegerField


foods = [{"name": "pizza", "rate": 4}, {"name": "burger", "rate": 5}]
# or
foods = Food.objects.all()  # where Food is a django model

structure = converter.structure(foods, list[FoodData])  
unstructure = converter.unstructure(structure, list) # this will make a list[dict]
```

same logic applies to `loads`
```py
dump = converter.dumps(structure)
load = converter.loads(dump, list[FoodData])
```
note that bson and toml don't support list serialization.

## Comparison
in comparison with how django forms and DRF serializers work, see the examples below

in django forms we do:
```py
form = MyForm(data)
form.is_valid()
clean_data = form.cleaned_data
```

in drf we do:
```py
serializer = MySerializer(data)
serializer.is_valid()
clean_data = serializer.validated_data

# to serialize data
content = JSONRenderer().render(serializer.data)
```

the cattrs equivalent of forms is like this:
```py
try:
    form = converter.structure(data, MyForm)  # where `MyForm` is a cattrs supported class (usually and attrs class)
except* ValueError:  # notice the `*`, this is an exception group (unless you configure cattrs otherwise)
    pass
clean_data = converter.unstructure(form)
```

or if working with json (or other formats)
```py
try:
    form = converter.loads(data, MyForm)  # take a json data and load it to python
except* ValueError:  # notice the `*`, this is an exception group (unless you configure cattrs otherwise)
    pass
clean_data = converter.unstructure(form)

# to serialize data
data = converter.structure(clean_data, MyForm)  # to dump data, structure it first
content = converter.dumps(data)
```

structuring and loading also validates the data, so no need for the extra step.

note that `converter.structure` raises `ValueError` as an exception group.


## Serializers
the basic `converter` you saw in basic usage section can only structure and unstructure, which is powerful, but we can do more.

`cattrs` comes with a set of [preconfigured converters](https://catt.rs/en/stable/preconf.html).

we ship our own version of these converters, which extends on top of cattrs' version, though we call them `serializer` to avoid some confusion.
these are available in `django_cattrs_fields.converters` directory:

* django_cattrs_fields.converters.bson
* django_cattrs_fields.converters.cbor2
* django_cattrs_fields.converters.json
* django_cattrs_fields.converters.msgpack
* django_cattrs_fields.converters.msgspec
* django_cattrs_fields.converters.orjson
* django_cattrs_fields.converters.pyyaml
* django_cattrs_fields.converters.tomlkit
* django_cattrs_fields.converters.ujson

just import `serializer` from each of these modules:

```py
from django_cattrs_fields.converters import converter
from django_cattrs_fields.converters.json import serializer


structure = converter.structure(human, Human)
dump: str | bytes = serializer.dumps(structure)  # takes an structured data, dumps a json string
load: Human = serializers.loads(dump, Human)  # takes a dumped data, and loads that as a structured data
data = converter.unstructure(load)  # a dictionary of the data, ready to be used.
```

it is important to note, while `serializer` objects also have `structure` and `unstructure` methods, they are considered internal API, 
since they are configured to feed encoding and decoding functionalities, 
they don't necessarily behave the way you would expect them to.

so in most scenarios you should import a `converter` and a `serializer` to handle their specific task, unless you are fully aware how your `serializer` behaves and can handle it yourself.

the only exception (currently) is the msgspec serializer, which doesn't implement any additional logic and works like a normal `converter`, 
tho if the need arises, this could change.

## work with django views
you can use the data models you made with this package instead of django forms or serializers

```py
from django_cattrs_fields.converters import converter
from django_cattrs_fields.converters.json import serializer


@define
class Human:
    id: UUIDField
    username: CharField
    email: EmailField
    slug: SlugField
    website: URLField
    age: IntegerField
    salary: FloatField
    birth_date: DateField
    signup_date: DateTimeField
    accurate_salary: DecimalField
    lunch_time: TimeField


def get_data(request):
    if request.method == "POST":
        if request.content_type in {"application/x-www-form-urlencoded", "multipart/form-data"}:
            structured_data = converter.structure({**request.POST.dict(), **request.FILES.dict()}, Human)  # handle html forms, and multipart data
        else:
            structured_data = serializer.loads(request.body, Human)  # handle json (or anything else)

        data: dict[str, Any] = converter.unstructure(structured_data)  # a dictionary of all the POST data (excluding data not covered by Human)

        return HttpResponse("done")
```
and just like that you have one view that handles html forms and json in one place

note that if `POST` data contains anything not in `Human`, it won't show up in the output data (such as csrf token, in this case)

also note that when working with APIs, depending on your client you might need to add `csrf_exempt` on you view.


## saving to database
one you unstructure your data, you have a dictionary of cleaned data.
then you can just pass that to your model and create your data

```py
data: dict[str, Any] = converter.unstructure(structured_data)

# either
obj = HumanModel(**dict)
obj.save()

# or
HumanModel.objects.create(**dict)
```


## nullable fields
by default all fields are required and passing a `None` value will raise an error
to make a field nullable, you can use a union 

```py
@define
class Product:
    name: CharField  # required
    discount: FloatField | None  # optional
```


## default values
to add a default value, the simplest way is to just add it via assignment

```py
@define
class Product:
    name: CharField  # required
    discount: FloatField = 5.1
```
for more advanced use check [default docs](https://www.attrs.org/en/stable/examples.html#defaults)

## field params
some fields like `DecimalField` can take some parameter about their data using `typing.Annotated`.

```py
from typing import Annotated

from attrs import define

from django_cattrs_fields.fields import DecimalField, CharField, Params

@define
class Product:
  name: CharField
  discount: Annotated[DecimalField, Params(decimal_max_digits=5, decimal_places=3)]
```

the use case of params differs depending on the field, in the case of Decimal field, `decimal_max_digits` as equivalent to django's DecimalField's `max_digits` parameter
and `decimal_places` is equivalent to `decimal_places` parameter, and are used when structuring the data to validate the decimal value.

like django, DecimalField's params are optional, some fields may require some params in the future.


## EmptyField
`EmptyField` is useful when supporting PATCH requests.

by default EmptyField hooks are disabled, it is recommended that you [create a specific converter](https://catt.rs/en/stable/basics.html#converters-and-hooks) for when you need EmptyField hooks, 
but if you want to use them on the converter provided by default, set `DCF_EMPTY_HOOKS` to `True` in your settings. note that this will only register the hooks for converter, not serializers (it's unlikely to use EmptyField hooks for serialization)

the reason to prefer a specific hook for EmptyField use is that, to make EmptyField possible we use a `hook_factory`, these kind of hooks will run anytime you call `unstructure`, even if no EmptyField is present.
while the overhead might be very small, it adds a layer of complexity over all your operations, so unless you are using `EmptyField`s everywhere, I recommend using a secondary converters.
converters are relatively cheap, and the recommended way to use cattrs is to have as many of them as you need.

to create a converter for EmptyField hooks:

```py
from django_cattrs_fields.converters.register_hooks import register_all_empty_unstructure_hooks
from django_cattrs_fields.converters import converter

empty_converter = converter.copy()  # or create a bare converter

register_all_empty_unstructure_hooks(empty_converter)

```

when using EmptyField hooks, if a field doesn't receive any data and has `Empty` as its value, it will be omitted when unstructuring.

```py
from django_cattrs_fields.fields import CharField, EmptyField, Empty

@define
class Human:
  name: CharField 
  age: IntegerField | EmptyField = Empty  # default to Empty, or provide Empty manually


struct = converter.structure({"name": "bob"})
# Human(name='bob', age=Empty)
unstruct = converter.unstructure(struct)
# {'name': 'bob'}
```

as you can see, since age is `Empty`, it won't be included in the resulting dictionary.

**Warning**: at the moment, `EmptyField` is only supported in unions that have only one other type, tho None is also supported, so:

* `CharField | EmptyField` works.
* `CharField | EmptyField | None` works.
* `CharField | IntegerField | EmptyField` doesn't work.

if complex types are required, register your custom hooks until we can figure out how to properly support this.
for inspiration, you can check `django_cattrs_fields.hooks.empty_hooks` to see how other hooks are made.

## validation
by default this package runs some validation when you are structuring your data
but to add any custom validators you can use attrs [built-in](https://www.attrs.org/en/stable/examples.html#validators) validation mechanism.

note that the validations we run are baked in structure hooks, so they will run in any situation.
these are validations that django also runs every time you use its data fields.
if you need to turn this off, just create a [new converter](https://catt.rs/en/stable/basics.html#converters-and-hooks)

## File Handling
this package comes with FileField you can use to work with files.
when an uploaded file is passed to this field (e.g: user POSTs some file), it goes through validation,
then an instance of django's `UploadedFile` is returned (usually a subclass of UploadedFile is used like `InMemoryUploadedFile`).

you can save this using the ORM or any other way you do with django.

when serving a File (e.g: user sends a GET request), an instance of django's `FieldFile` should be passed (django ORM does this automatically)
in this case our hooks will return the url of the file.

note that this behavior is different in django and DRF
django returns the whole `FieldFile` object (could be useful with templates), DRF is configurable, it either returns the url or the file name.

if you require a different behavior, you can change this by hooking your logic and set `DCF_FILE_HOOKS` to False in your settings file, 
this will disable all file related hooks.



## contribution
I appreciate any help with this project, but please follow Django's Code of Conduct
if you have ideas or have found a bug please open an [issue on github](https://github.com/amirreza8002/django-cattrs-fields/issues/new)

to help with development follow these steps:
1. fork the repository from [github](https://github.com/amirreza8002/django-cattrs-fields).
2. clone the project from your fork.
3. install the package with one of the following commands:
  * `uv sync --group dev`
  * `uv sync --group dev --group ipython`
  * `uv sync --group dev --group prek`
  * `uv sync --group dev --group test`
you can combine them together or just use `uv sync --all-groups` to one-shot.
4. run `prek install` or `pre-commit install` depending on your choice.

if you are contributing new code, please make sure to add some tests for it.

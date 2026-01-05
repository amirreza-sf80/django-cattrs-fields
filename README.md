# django-cattrs-fields

**Note**: this is a very experimental project, i'm mostly navigating and discovering how this could work,
as much as any help and feedback is appreciated, please do not use in a production environment.

bring [cattrs](https://github.com/python-attrs/cattrs) support to the django world.

this project is the first step of many, it is intendened to be minimal, only adding data type support.

### current data types
* BooleanField
* CharField
* EmailField
* SlugField
* URLField
* UUIDField
* IntegerField
* FloatField
* DateField
* DateTimeField


### installing
this is not packaged to pypi yet, for using you need to clone the repository first.

then install the package by running `uv sync` or `uv sync --extra <group name>` where group name is one of optional-dependencies listed in pyproject.toml.

if you want a one shot install use `uv sync --all-extras`



### basic usage:
data model classes are `attrs` classes, so anything you find in [attrs](https://www.attrs.org/en/stable/index.html) docs also applies here.
we also follow cattrs, so anything in their [docs](https://catt.rs/en/stable/index.html) also applies

```py
import uuid
from datetime import date, datetime

from attrs import define

from django-cattrs-fields.converters import converter
from django_cattrs_fields.fields import (
  BooleanField, 
  CharField, 
  EmailField, 
  SlugField, 
  URLField, 
  UUIDField, 
  IntegerField, 
  FloatField, 
  DateField,
  DateTimeField
)

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


human = {
    "id": uuid.uuid4(),
    "username": "bob",
    "email": "bob@email.com",
    "slug": "bo-b",
    "website": "https://bob.com",
    "age": 25,
    "salary": 1000.43,
    "birth_date": date(year=2000, month=7, day=3),
    "signup_date": datetime.now()
}

structure = converter.structure(human, Human)  # runs structure hooks and validators, then creates an instance of `Human`
normal_data = converter.unstructure(structure)  # runs unstructure hooks, then makes a dict similar to `human` (or what you tell it to), no validators run.
```

### serializers
the basic converter you saw in basic usage section can only structure and unstructure, which is powerful, but we can do more
`cattrs` comes with a set of [preconfigured converters](https://catt.rs/en/stable/preconf.html).

we ship our own version of these converters, which extends on top of cattrs' version
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

just import `converter` from each of these modules

```py
from django_cattrs_fields.converters.json import converter


structure = converter.structure(human, Human)  
dump: str | bytes = converter.dumps(structure)  # takes an structured data, dumps a json string
load: Human = converter.loads(structure, Human)  # takes a dumped data, and loads that as a structured data
```

### work with django views
you can use the data models you made with this package instead of django forms or serializers

```py
from django_cattrs_fields.converters.json import converter


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


def get_data(request):
    if request.method == "POST":
        if request.content_type in {"application/x-www-form-urlencoded", "multipart/form-data"}:
            structured_data = converter.structure({**request.POST.dict(), **request.FILES.dict()}, Human)  # handle html forms, and multipart data
        else:
            structured_data = converter.loads(request.body, Human)  # handle json (or anything else)

        data: dict[str, Any] = converter.unstructure(structured_data)  # a dictionary of all the POST data (excluding data not covered by Human)

        return HttpResponse("done")
```
and just like that you have one view that handles html forms and json in one place

note that if `POST` data contains anything not in `Human`, it won't show up in the output data (such as csrf token, in this case)

also note that when working with APIs, depending on your client you might need to add `csrf_exempt` on you view.


### saving to database
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


### nullable fields
by default all fields are required and passing a `None` value will raise an error
to make a field nullable, you can use a union 

```py
@define
class Product:
    name: CharField  # required
    discount: FloatField | None  # optional
```


### default values
to add a default value, the simplest way is to just add it via assignment

```py
@define
class Product:
    name: CharField  # required
    discount: FloatField = 5.1
```
for more advanced use check [default docs](https://www.attrs.org/en/stable/examples.html#defaults)


### validation
be default this package runs some validation when you are structuring your data
but to add any custom validators you can use attrs [built-in](https://www.attrs.org/en/stable/examples.html#validators) validation mechanisem.

note that the validations we run are baked in structure hooks, so they will run in any situation.
these are validations that django also runs every time you use it's data fields.
if you need to turn this of, just create a [new converter](https://catt.rs/en/stable/basics.html#converters-and-hooks)


## contribution
I appreate any help with this project, but please follow django's code of conduct
if you have ideas or have found a bug please open an [issue on github](https://github.com/amirreza8002/django-cattrs-fields/issues/new)

to help with development follow these steps:
1. fork the repository from [github](https://github.com/amirreza8002/django-cattrs-fields)
2. clone the project from your fork
3. install the package with one of the following commands:
  * `uv sync --group dev` 
  * `uv sync --group dev --group ipython`
  * `uv sync --group dev --group prek`
  * `uv sync --group dev --group test`
you can combine them together or just use `uv sync --all-groups` to one shot
4. run `prek install` or `pre-commit install` depending on your choice.

if you are contributing new code, please make sure to add some tests for it.

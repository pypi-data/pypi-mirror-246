import pydantic


class SubClass(pydantic.BaseModel):
    first: str
    second: bool
    optional_int: int = None


class Class(pydantic.BaseModel):
    subclass: SubClass
    optional_subclass: SubClass = None
    second_subclass: 'SecondSubClass'
    optional_second_subclass: 'SecondSubClass' = None


class SecondSubClass(pydantic.BaseModel):
    first: str


Class.model_rebuild(force=True)


def test_pydantic():
    Class(subclass={'first': '1', 'second': True, 'optional_int': 2},
          second_subclass={'first': '1'})
    Class(subclass=SubClass(first='1', second=True), second_subclass=SecondSubClass(first='1'))

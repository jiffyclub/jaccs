import pytest

from jaccs import access, access_factory
from conftest import json_obj, json_list

JSON_OBJ = json_obj()
JSON_LIST = json_list()


@pytest.mark.parametrize('expr, result', [
    ('_', JSON_OBJ),
    ('_.key', JSON_OBJ['key']),
    ('_.sequence[0]', JSON_OBJ['sequence'][0]),
    ('_.mapping.key', JSON_OBJ['mapping']['key']),
    ('_.mapping.sequence[-1]', JSON_OBJ['mapping']['sequence'][-1])
])
def test_access_on_object(json_obj, expr, result):
    assert access(json_obj, expr) == result


@pytest.mark.parametrize('expr, result', [
    ('_', JSON_LIST),
    ('_[0]', JSON_LIST[0]),
    ('_[1][-1]', JSON_LIST[1][-1]),
    ('_[2].key', JSON_LIST[2]['key'])
])
def test_access_on_list(json_list, expr, result):
    assert access(json_list, expr) == result


def test_access_default_keys(json_obj):
    with pytest.raises(KeyError):
        access(json_obj, '_.missing', use_default=False)

    result = access(json_obj, '_.missing', use_default=True, default='default')
    assert result == 'default'


def test_access_default_indexes(json_obj):
    with pytest.raises(IndexError):
        access(json_obj, '_.sequence[99]', use_default=False)

    result = access(
        json_obj, '_.sequence[99]', use_default=True, default='default')
    assert result == 'default'


def test_access_factory(json_obj):
    _access = access_factory('_.mapping.key')
    assert _access(json_obj) == 'value'

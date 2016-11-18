import pytest


@pytest.fixture(scope='session')
def json_obj():
    return {
        'key': 'value',
        'sequence': [1, 2, 3],
        'mapping': {
            'key': 'value',
            'sequence': [4, 5, 6]
        }
    }


@pytest.fixture(scope='session')
def json_list():
    return [
        'value',
        [1, 2, 3],
        {'key': 'value'}
    ]

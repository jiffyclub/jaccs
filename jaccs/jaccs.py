"""
Utilities for accessing values within JSON objects or arrays.

"""
import collections


class Dots(object):
    """
    Wraps dictionaries or lists to implement attribute access for dict keys.

    Scalar-like objects (strings, numbers, etc) are returned as is,
    but nested sequences/mappings are wrapped again to support further
    attribute-style access.
    Use the _ attribute to access the raw wrapped Python object.

    Parameters
    ----------
    data : mapping or sequence
        Data object to wrap for access.

    Example
    -------
    >>> d = Dots({'a': {'b': [1, 2, 3]}})
    >>> d.a.b[1]
    2
    >>> d.a
    Dots({'b': [1, 2, 3]})
    >>> d.a._
    {'b': [1, 2, 3]}

    """
    def __init__(self, data):
        self._data = data

    @property
    def _(self):
        """Access the wrapped Python object."""
        return self._data

    @classmethod
    def get_value(cls, data, item):
        """
        Get the value at index ``item`` from the ``data`` object.

        If the resulting value appears to be a scalar it is returned,
        but if it appears to be another container it is wrapped before
        being returned.

        """
        result = data[item]
        if (isinstance(result, (collections.Mapping, collections.Sequence)) and
                not isinstance(result, str)):
            return cls(result)
        else:
            return result

    def __getitem__(self, key):
        return self.get_value(self._data, key)

    def __getattr__(self, attr):
        if not isinstance(self._data, collections.Mapping):
            raise TypeError('dot access only available on dictionary-like objects')
        return self.get_value(self._data, attr)

    def __repr__(self):
        return 'Dots({!r})'.format(self._data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._data == other._data
        else:
            return NotImplemented


def _compile_expr(expr):
    """
    Turns a Python expression into a code object. Non-string inputs are
    passed through unchanged so this can be safely called on already
    compiled expressions.

    """
    if isinstance(expr, str):
        return compile(expr, '<string>', mode='eval')
    return expr


def access_factory(expr, use_default=False, default=None):
    """
    Create a function that will take a JSON object and retrieve
    data according to the arguments here.

    Parameters
    ----------
    expr : str
        Access string describing path into a JSON object.
        Can be any valid Python expression, use ``_`` to represent
        the JSON object.
    use_default : bool, optional
        If True, the value of ``default`` will be returned in instances
        when a KeyError or IndexError occurs while evaluating ``expr``.
    default : bool, optional
        Default value to return when use_default is True and a KeyError
        or IndexError occurs while evaluating ``expr``.

    Returns
    -------
    function
        Takes a single argument of a JSON object and returns data from
        the object according to the arguments here.

    Examples
    --------
    >>> access_ = access_factory('_.a.b[2]')
    >>> access_({'a': {'b': [1, 2, 3]}})
    3
    >>> access_ = access_factory('_.a.c', use_default=True, default=2)
    >>> access_({'a': {'b': 1}})
    2

    """
    compiled_expr = _compile_expr(expr)

    def _access(dict_or_list):
        if expr == '_':
            return dict_or_list

        try:
            result = eval(compiled_expr, {}, {'_': Dots(dict_or_list)})
        except (KeyError, IndexError):
            # allow defaults for missing fields
            if use_default:
                result = default
            else:
                raise

        if isinstance(result, Dots):
            result = result._data

        return result

    return _access


def access(dict_or_list, expr, use_default=False, default=None):
    """
    Retrieve whatever is at some path into a JSON object.

    Parameters
    ----------
    dict_or_list : sequence or mapping
        The object from which to retrieve data.
    expr : str
        Access string describing path into ``dict_or_list``.
        Can be any valid Python expression, use ``_`` to represent
        ``dict_or_list``.
    use_default : bool, optional
        If True, the value of ``default`` will be returned in instances
        when a KeyError or IndexError occurs while evaluating ``expr``.
    default : bool, optional
        Default value to return when use_default is True and a KeyError
        or IndexError occurs while evaluating ``expr``.

    Examples
    --------
    >>> access({'a': {'b': [1, 2, 3]}}, '_.a.b[2]')
    3
    >>> access({'a': {'b': 1}}, '_.a.c', use_default=True, default=2)
    2

    """
    _access = access_factory(expr, use_default=use_default, default=default)
    return _access(dict_or_list)


def spec_to_records(spec, seq_of_json):
    """
    Combine a specification of JSON access strings with a sequence of
    JSON objects to create a sequence of records.

    Parameters
    ----------
    spec : dict
        Dictionary in which keys are paired with dictionaries or strings
        specifying how to access an item from the JSON objects in
        ``seq_of_json``. Dictionaries must have at least an ``expr``
        key and may optionally have ``use_default`` and ``default`` keys.
        See the ``access`` documentation for descriptions of the values.
        If the dict values are strings they are used as the ``expr``.
    seq_of_json : iterable
        Any iterable of JSON objects.

    Yields
    ------
    dict
        One dictionary for each value in ``seq_of_json``. Each will have
        the same keys as ``spec`` and values pulled from the JSON
        objects according to the expressions in ``spec``.

    Examples
    --------
    >>> spec = {'b': '_.a.b', 'c': {'expr': '_.a.c', 'use_default': True, 'default': 4}}
    >>> json = [{'a': {'b': 1, 'c': 2}}, {'a': {'b': 3}}]
    >>> list(spec_to_records(spec, json))
    [{'c': 2, 'b': 1}, {'c': 4, 'b': 3}]

    """
    access_dict = {
        key: access_factory(**spec_item)
        if isinstance(spec_item, dict) else access_factory(spec_item)
        for key, spec_item in spec.items()}

    for json_item in seq_of_json:
        yield {
            key: _access(json_item)
            for key, _access in access_dict.items()}

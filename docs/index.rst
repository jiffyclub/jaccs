.. Jaccs documentation master file, created by
   sphinx-quickstart on Thu Dec 15 21:28:54 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Jaccs - JSON Access Strings
===========================

Jaccs allows you to pull data from JSON objects using string Python
expressions. For example::

    >>> from jaccs import access
    >>> access({'a': 'b': [{'c': 1}, {'c': 2}]}, '_.a.b[1].c')
    2

This is expected to be most useful for combining specifications stored in
external text files (say JSON or YAML) with data objects in Python.

Installation
------------

The best way to install Jaccs is via PyPI::

    pip install jaccs

For the latest you can install from Github master with::

    pip install https://github.com/jiffyclub/jaccs/archive/master.zip

Source code is on Github at https://github.com/jiffyclub/jaccs.

Access String Syntax
--------------------

Access strings must be valid Python expressions, and the result returned
by :py:func:`~jaccs.access` will be the result of calling
`eval <https://docs.python.org/3/library/functions.html#eval>`__
on the expression. The JSON object is represented by an underscore in
the expression. Jaccs wrapps the JSON object so that dictionary keys can
be accessed via attributes::

    >>> access({'a': {'b': 'z'}}, '_.a.b')
    'z'

List items can be accessed via indexing::

    >>> access(['x', 'y', 'z'], '_[0]')
    'x'

Not all dictionary keys are valid attribute names so dictionary values
can also be accessed with the usual brackets::

    >>> access({'a b c': 'x y z'}, '_["a b c"]')
    'x y z'

Expressions need not be limited to data access, they can access Python's
builtin functions and build their own arbitrarily complex objects.
If for some reason you need access to the wrapped JSON object use the
``._`` attribute::

    >>> access({'data': [1, 2, 3]}, '{"data": _.data._, "sum": sum(_.data._)}')
    {'data': [1, 2, 3], 'sum': 6}

API
---

access
~~~~~~

``access`` is the simplest way to combine a JSON object and
a string specification for data access.
The ``use_default`` and ``default`` parameters can be used to return a default
value when a key or array index is not found within the JSON object.
Unless ``use_default`` is specified ``KeyError`` or ``IndexError`` is raised
for missing keys/indices.

.. autofunction:: jaccs.access

access_factory
~~~~~~~~~~~~~~

If you intend to use the same access string repeatedly on a sequence of
JSON objects it can be more performant to parse and compile the expression
ahead of time.
The ``access_factory`` function does that and returns a new function ready
to process JSON objects according to the configuration passed
to ``access_factory``.

.. autofunction:: jaccs.access_factory

spec_to_records
~~~~~~~~~~~~~~~

``spec_to_records`` allows you to stream a sequence of JSON objects against
a dictionary of access strings (a spec), yielding dictionaries with the same keys
as the spec holding values pulled from the JSON objects.

.. autofunction:: jaccs.spec_to_records

Dots
~~~~

``Dots`` is a class used internally by Jaccs to translate attribute lookups
into normal key-based access on dictionaries.
It's the workhorse used when evaluating JSON access strings.
It's exposed here in case folks have a case for using it to write less verbose
dictionary access code and don't want to use any of the functions documented
above.

.. autoclass:: jaccs.Dots
   :members: _

Index
=====

* :ref:`modindex`

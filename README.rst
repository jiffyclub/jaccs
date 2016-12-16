Jaccs - JSON Access Strings
===========================

.. image:: https://travis-ci.org/jiffyclub/jaccs.svg?branch=master
   :target: https://travis-ci.org/jiffyclub/jaccs

Jaccs allows you to pull data from JSON objects using string Python
expressions. For example::

    >>> from jaccs import access
    >>> access({'a': 'b': [{'c': 1}, {'c': 2}]}, '_.a.b[1].c')
    2

This is expected to be most useful for combining specifications stored in
external text files (say JSON or YAML) with data objects in Python.

Documentation is at https://jiffyclub.github.io/jaccs/.

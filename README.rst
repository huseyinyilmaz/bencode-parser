bencode-parser |build|_
============================

Bencode parser for python.

For more information about bencode format please refer to wiki_page_

INSTALLATION
============

::

   $ pip install bencode-parser

USAGE
=====

::

   >>> import bencode
   >>> bencode.decode('3:abc')
   'abc'
   >>> bencode.decode('i123e')
   123
   >>> bencode.decode('li1ei2ei3ee')
   [1, 2, 3]
   >>> bencode.decode('d1:1i1e1:2i2e1:3i3ee')
   {'1': 1, '3': 3, '2': 2}
   >>> bencode.encode('abc')
   '3:abc'
   >>> bencode.encode(123)
   'i123e'
   >>> bencode.encode([1,2,3])
   'li1ei2ei3ee'
   >>> bencode.encode({'1': 1, '3': 3, '2': 2})
   'd1:1i1e1:3i3e1:2i2ee'


.. |build| image:: https://travis-ci.org/huseyinyilmaz/django-numerics.png
.. _build: https://travis-ci.org/huseyinyilmaz/django-numerics

.. _wiki_page: https://en.wikipedia.org/wiki/Bencode

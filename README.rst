=======
notizen
=======

Indexing and searching of personal notes.

Installation
============

.. image:: https://img.shields.io/pypi/dw/stups-piu.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: PyPI Downloads

.. image:: https://img.shields.io/pypi/v/stups-piu.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/l/stups-piu.svg
   :target: https://pypi.python.org/pypi/notizen/
   :alt: License

.. code-block:: bash

	$ sudo pip3 install --upgrade notizen

Usage
=====

First index some notes:

.. code-block:: bash

	$ notizen updatedb my-notes/
	$

Then you can search for all files with tag python:

.. code-block:: bash

	$ notizen locate python
	2 matching files under tag "python":
        /foo/bar/my-notes/python_annotations.md
        /foo/bar/my-notes/async-python.md
    $

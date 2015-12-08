Install for development
=======================

git clone...
virtualenv...
pull requests, etc.
checking for code linting, etc.

To Do
=====

1. Look for several tags
2. Conditions in the searches: not, and, or
3. Look in title, date, short description -> this needs an index redesign, or delegating indexing in (e.g.) ElasticSearch.
4. Delegate indexing and search in ElasticSearch.
5. Index more information: title, filename, short description -> only in notizen.updatedb.get_info_from_file()
6. Search using more info (from 5).
7. Return different than 0 to the shell if error.
8. Use different index/store/search backends: ES, pickle files, etc.
9. What about checking?
10. provide a tested packaging setup: setup.py, LICENSE, etc.
11. Badges in README.rst
12. Switch debug level for logger.

Milestones
==========

Version 1:
Version 2: Go to ElasticSearch

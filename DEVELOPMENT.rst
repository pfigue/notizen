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
11. Badges in README.rst fix them
12. Switch debug level for logger.
13. --flag to see files w.o tagging

Milestones
==========

# Going for 1.0.0

1. Master branch: Version 1.0.0: fix packaging, check for fixmes, remove dead code and debug traces and change logging level and go. See Checklist packaging in notes.

	1. Prepare setup.py. Test it. (done, but it can be better tested; are there disposable test cheeseshop?)
	2. Check for FIXMEs (done)
	3. Check for BUGs (done)
	4. Check for dead code (done)
	5. Check for function docu. (done)
	6. Change logging level.
	1. Tox setup (skip)
	2. pyflakes (done), pylint
	3. pyroma (done. was it right?)
	8. blog about the notes i write: here they are, and the have this format and I can use this and that program to search.


## Heading to 1.0.1

2. New branch 1.0.1: get_info_from_file returns more things, like title, short description, etc.; unit tests for get_info_from_file; bug update_tags_index; 

	1. --index-path option (done)
	2. unit tests for updatedb.get_info_from_file (done)


branch2: ``notize updatedb --show-untagged`` add that --show-untagged option

branch3: use a config file (INI or YAML). Atm. just to locate where will be the index. Provide a --config option. Prepare to receive parameters for ES.
	3. Use a config file. Yaml? INI?
	4. --config <path> to avoid using (default) ~/.config/notizen/...
	9. --configfile <path> Be able to provide a config file, to have different indices. Also --profile <name> to have several kind of notes, like --profile work --profile personal, --profile gardening etc. Then in the config file:
	[gardening]
	prefix: gardening
	and that will refer to gardening.pickle or to gardening index in ES.

branch4: --profile and check different profiles from the config file.

	4. error: invalid command 'bdist_wheel'
	10. Tested with pypy3.2, but had to install the linux 64bits binaries as there is no package for ubuntu.

	5. provide testing samples. with 1 tag line, w/o, with several. markdown, no markdown, etc. -> how to test it efficiently?
	6. learn to use the Mock objects.
	7. Write docs on how to write the notes. provide some examples.
	9. Python 2?

branch5: accept rst format and the different markdown/rst formats. Accept ; as separator instead of ,.

3. skip directories. config file.yaml (e.g. to point to a different index)?; unit tests for add_file_to...; show files which have no tags

3. Version 2: Go to ElasticSearch. Stateful ES container?

4. Travis CI is free for open source projects.

# coding: utf-8

import os
from tempfile import mkstemp
from notizen.updatedb import get_info_from_file as giff


def tmpfile(content: str, prefix: str='test_updatedb') -> str:
	'''Creates a temporary file with the given :content.
	Returns the path to the file.
	You are responsible of removing it later.'''

	(f, name) = mkstemp(prefix=prefix, text=True)
	os.write(f, content.encode('utf-8'))
	os.close(f)
	return name


# Tags (and Keywords) tests

def test_giff_oneTag():
	'''Check if it can find one tag'''
	data = '''first line
	tags: python'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('tags', None) == ['python']


def test_giff_twoTags():
	'''Check if it can find tags when there are two'''
	data = '''first line
	tags: python, pypy'''
	fn = tmpfile(data)
	result = giff(fn)
	result = result.get('tags', None)
	result = set(result)
	os.unlink(fn)
	expected = frozenset(['python', 'pypy'])
	assert result == expected


def test_giff_noTags():
	'''Check if it doesn't crash when there are no tags'''
	data = '''first line'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('tags', None) == None


def test_giff_emptyTags():
	'''Check if it doesn't crash when there the tags label is empty'''
	data = '''first line
	tags:

	body of the document'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('tags', None) == ['']
	# FIXME i think this should be returning None,
	# or the previous should return this empty list.

def test_giff_twiceTags():
	'''Check if there are several tag lines'''
	data = '''first line
	tags: python
	tags: broccoli'''
	fn = tmpfile(data)
	result = giff(fn)
	result = result.get('tags', None)
	result = set(result)
	os.unlink(fn)
	expected = frozenset(['python', 'broccoli'])
	assert result == expected
	# FIXME right behaviour? take just the last one, or all?

def test_giff_oneKeyword():
	'''Check if it works with Keywords: instead of Tags:'''
	data = '''first line
	keywords: python'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('tags', None) == ['python']

# Didn't check for case insensitive, but I think re module can be trusted.

# Title tests

def test_giff_oneTitle():
	'''Check if it can find one tag'''
	data = '''title: first line

	contents'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('title', None) == 'first line'


def test_giff_twoTitles():
	'''Check if it can find one tag'''
	data = '''title: first line
	title: mistake

	contents'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('title', None) == 'mistake'

def test_giff_noTitle():
	'''Check if it can find one tag'''
	data = '''

	contents'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('title', None) == None

def test_giff_emptyTitle():
	'''Check if it can find one tag'''
	data = '''title:

	contents'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('title', None) == ''

def test_giff_multilineSummary():
	'''Check if it can find one tag'''
	data = '''summary: this is a long line without a break. It should behave the same as title.

	contents'''
	fn = tmpfile(data)
	result = giff(fn)
	os.unlink(fn)
	assert result.get('summary', None) == 'this is a long line without a break. It should behave the same as title.'
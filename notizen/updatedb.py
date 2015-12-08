#!/usr/bin/env python
#coding: utf-8

"""
Goal(s):
	- Walk all the notes fetching:
		- tags
		- file name
	- Store the cPickle in some ~/.config/notizen/notes-index.cpickle
	- Make a command, clickclick.
"""

import re
import os
import logging
from os import path
from notizen import indices


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
RE_TAG = re.compile(r'^\s*tags:(.*)$', re.IGNORECASE)
RE_FILE = re.compile(r'^.*\.md$', re.IGNORECASE)
INDEX_FILEPATH = 'index.pickle'  # FIXME use click get config file;


def get_info_from_file(filepath: str) -> dict:
	with open(filepath, 'r') as f:
		ten_first_lines = f.readlines()[:10]
	msg = '10 first lines: "{}"'
	msg = msg.format(ten_first_lines)
	# LOGGER.debug(msg)
	info = {'filepath': filepath}
	for line in ten_first_lines:
		result = RE_TAG.match(line)
		if result:
			# LOGGER.debug('RE_TAG!')
			tags_str = result.groups()[0]
			# LOGGER.debug(tags_str)
			tags_l = tags_str.split(',')
			# LOGGER.debug(str(tags_l))
			tags_l = [t.strip() for t in tags_l]
			# LOGGER.debug(str(tags_l))
			tags_l += info.get('tags', [])
			info.update({'tags': tags_l})
	return info


# def updatedb():
# 	(tags_index, ) = load_indices(where_from=INDEX_FILEPATH)
# 	LOGGER.debug(tags_index)

# 	for (root, dirs, files) in os.walk('../notes/'):
# 		for filepath in files:
# 			filepath = path.join(root, filepath)
# 			if not RE_FILE.match(filepath):
# 				continue
# 			#
# 			LOGGER.debug('processing: {}'.format(filepath))
# 			info = process_one_file(filepath)
# 			LOGGER.debug(info)
# 			add_file_to_tag_index(tags_index, info)

# 	LOGGER.debug(tags_index)
# 	save_indices(tags_index=tags_index, where=INDEX_FILEPATH)


def update_tags_index(tags_index:dict, notes_path: str) -> None:
	'''
	BUG: it can add new files, but can't remove those files which lost a tag.
	'''
	LOGGER.debug('update_tags_index begins: in {}, {}.'.format(notes_path, len(tags_index)))

	for (root, dirs, files) in os.walk(notes_path):
		# FIXME skip .git .ipynb_checkpoints dirs.
		for filepath in files:
			filepath = path.join(root, filepath)
			if not RE_FILE.match(filepath):
				# LOGGER.debug('skipping file {}.'.format(filepath))
				continue  # FIXME test this.
			#
			# LOGGER.debug('processing: {}'.format(filepath))
			fileinfo = get_info_from_file(filepath)  # FIXME what if no tags?
			# LOGGER.debug(fileinfo)
			indices.add_file_to_tag_index(tags_index, fileinfo)

	LOGGER.debug('update_tags_index ends: {}, {}'.format(notes_path, len(tags_index)))

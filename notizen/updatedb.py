#!/usr/bin/env python
# coding: utf-8

"""
FIXME
"""

import re
import os
import logging
from os import path
from notizen import indices


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
# FIXME also `keywords:`
RE_TAG = re.compile(r'^\s*tags:(.*)$', re.IGNORECASE)
# FIXME also *.rst
RE_FILE = re.compile(r'^.*\.md$', re.IGNORECASE)


def get_info_from_file(filepath: str) -> dict:
    '''Provides a dictionary with the info extracted from a file.
    Currently only the tags and the path to the file.'''

    with open(filepath, 'r') as f:
        ten_first_lines = f.readlines()[:10]
    info = {'filepath': filepath}
    for line in ten_first_lines:
        result = RE_TAG.match(line)
        if result:
            tags_str = result.groups()[0]
            tags_l = tags_str.split(',')
            tags_l = [t.strip() for t in tags_l]
            tags_l += info.get('tags', [])
            info.update({'tags': tags_l})
    return info


def update_tags_index(tags_index: dict, notes_path: str) -> None:
    '''Walks all the directory path, extracts info for each
    Markdown file and updates the Tags Index provided.'''

    for (root, dirs, files) in os.walk(notes_path):
        # FIXME skip .git .ipynb_checkpoints dirs.
        for filepath in files:
            filepath = path.join(root, filepath)
            if not RE_FILE.match(filepath):
                continue
            # FIXME what if no tags?
            fileinfo = get_info_from_file(filepath)
            indices.add_file_to_tag_index(tags_index, fileinfo)

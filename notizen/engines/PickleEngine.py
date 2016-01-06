# coding: utf-8


import logging
import pickle
from notizen import utils
from notizen.engines import interfaces


LOGGER = logging.getLogger(__name__)


class PickleEngine(interfaces.NotizenEngine):
    '''move indice.py into here'''

    @staticmethod
    def _load_indices(where_from: str) -> tuple:
        '''Loads the indices from the file refered by :where_from
        and returns a tuple: (tags_index, ).
        Should not find the file, it will return empty indices.'''

        try:
            with open(where_from, 'br') as f:
                idx = pickle.load(file=f)
            tags_index = idx['tags_index']
        except FileNotFoundError:
            tags_index = {}
            LOGGER.info('File "{}" was not found.'.format(where_from))
        return (tags_index, )

    @staticmethod
    def _save_indices(tags_index: dict, where: str) -> None:
        '''Save the indices into the file refered by :where.'''

        idx = {
            'tags_index': tags_index,
        }
        with open(where, 'bw') as f:
            pickle.dump(obj=idx, file=f, protocol=-1)

    @staticmethod
    def _add_file_to_tag_index(tags_index: dict, fileinfo: dict) -> None:
        '''Adds entries into the Tags Index'''
        tags_l = fileinfo.get('tags', None)
        if not tags_l:  # File has no tags
            return
        filepath = fileinfo['filepath']
        for tag in tags_l:
            file_l = tags_index.get(tag, [])
            file_l = list(set(file_l + [filepath, ]))
            tags_index[tag] = file_l            

    def __init__(self, filepath):
        self.tags_index = None
        self.filepath = filepath
        self.modified_indices = False
        self.start()

    def start(self):
        '''load pickle file'''
        (self.tags_index, ) = self._load_indices(self.filepath)

    def index_doc(self, doc):
        '''Update data structures.'''
        self.modified_indices = True
        self._add_file_to_tag_index(self.tags_index, doc)

    def search_by_tags(self, tag):
        '''look in the tag index'''
        matching_files = self.tags_index.get(tag, None)
        return matching_files

    def shutdown(self):
        '''save indices into pickle file'''
        if not self.modified_indices:
            LOGGER.info('No index changed.')
        else:
            self._save_indices(self.tags_index, self.filepath)

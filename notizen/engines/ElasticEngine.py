# coding: utf-8


import logging
import elasticsearch
import elasticsearch_dsl
from notizen import utils
from notizen.engines import interfaces


LOGGER = logging.getLogger(__name__)


class ElasticEngine(interfaces.NotizenEngine):
    def __init__(self, host, port, index_name):
        self.es = None
        self.index_name = index_name
        self.need_to_create_index = True
        self.start(host, port)

    def start(self, host, port):
        '''xxx'''
        # Get an ES handler.
        LOGGER.debug('going to connect..')
        pp = {
            'host': host,
            'port': port,
            'use_ssl': False,  # FIXME
        }
        # utils.cprint(pp)
        self.es = elasticsearch.Elasticsearch([pp,])
        LOGGER.debug('connected!')

    def _create_index(self):
        # Create index. Delete it if it already exists.
        msg = 'Dropping and recreating index {}!'.format(self.index_name)
        LOGGER.debug(msg)
        if self.es.indices.exists(self.index_name):
            self.es.indices.delete(index=self.index_name)
            LOGGER.debug('removed first!')
        self.es.indices.create(index=self.index_name)
        LOGGER.debug('created index!')

    def index_doc(self, doc):
        if not self.es:
            raise RuntimeError('No ElasticSearch instance!')
        if self.need_to_create_index:
            self._create_index()
            self.need_to_create_index = False
        LOGGER.debug('indexing something...')
        self.es.index(index=self.index_name, doc_type='note', body=doc)

    def search_by_tags(self, tag):
        '''query ES'''

        q = elasticsearch_dsl.Search(using=self.es, index=self.index_name) \
            .query('match', tags=tag)
        r = q.execute()
        matching_files = None if not r else [hit._d_['filepath'] for hit in r] 
        return matching_files

    def shutdown(self):
        '''something to do here?'''
        LOGGER.debug('shutting down.')
        pass


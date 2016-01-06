# coding: utf-8


import logging
from notizen import utils


LOGGER = logging.getLogger(__name__)


class NotizenEngine(object):
    def start(self):
        pass

    def index_doc(self, doc):
        pass

    def search_by_tags(self, tag):
        pass
        # FIXME define what the implementation should do.
        # e.g. should print something? or just return a list/tuple?

    def shutdown(self):
        pass

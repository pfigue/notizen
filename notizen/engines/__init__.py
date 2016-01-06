# coding: utf-8


from .ElasticEngine import ElasticEngine
from .PickleEngine import PickleEngine


def get_engine(profile: dict) -> object:
    '''Given a config profile, it will return an Engine sub object'''
    # utils.cprint(profile)
    engine = profile['engine']['name']
    if engine == 'pickle':
        index_path = None
        if index_path is None:  # If not provided in the CLI, FIXME
            index_path = profile['engine']['file']  # then take it.
        if index_path is None:  # If still not defined, set default.
            index_path = INDICES_FILE_PATH
        # utils.cprint(index_path)
        ng = PickleEngine(index_path)
    elif engine == 'elasticsearch':
        es_host = profile['engine']['host']
        es_port = profile['engine']['port']
        es_index = profile['name']
        ng = ElasticEngine(es_host, es_port, es_index)
    return ng
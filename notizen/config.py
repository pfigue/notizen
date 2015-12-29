# coding: utf-8


import yaml
from notizen import utils

# text = """- profile:
#     - name: noti1
#     - path: /path/to/noti1
#     - engine:
#         - name: elastic
#         - host: noti1-elastic
#         - port: 9200
#         - index_name: index-noti1

# - profile:
#     - name: noti2
#     - path: /path/to/noti2
#     - engine:
#         - name: pickle
#         - file: /path/to/pickle

# - default: noti2
# """


def flat_list(l: list):
    """NOTE: can not be duplicated in the list. If there are, the last one will be used."""
    print(l)
    d = dict()
    for e in l:
        utils.cprint(e, '!!')
        if type(e) == dict:
            d.update(e)
        else:
            d.update({e: None})

    utils.cprint(d, '%%')
    print('%% ',d.keys())
    for e in d.keys():
        # print('** d[e]=%s,%s' % (d[e], type(d[e])))
        utils.cprint(d[e], '**')
        if type(d[e]) == list:
            d[e] = flat_list(d[e])  # FIXME be careful with recursivity
    utils.cprint(d, '%%')
    return d
    #params = profile['profile']
    #print(params)


def process_yaml(text: str):
    default = None
    profiles = dict()
    r = yaml.load(text)
    for k in r:
    # print(k)

        r = k.get('profile', None)
    # print('this is k', k)
        if r:
            new_profile = flat_list(r)
            new_profile_name = new_profile['name']
            if profiles.get(new_profile_name, None):
                print('Warning: profile already exists')  # FIXME old, new one.
            profiles[new_profile_name] = new_profile  # FIXME does it exist already?
            # insert...
            continue

        r = k.get('default', None)
        if r:
            if default:
                print('Warning: default profile more than once: {} and now {}.')
            default = r
            continue

        print('Wrong KEY in config!')

    if not default:
        print('Error message!')  # FIXME Or not. compulsory?
    return (default, profiles)


def get_profile(text: str, profile_name: str=None) -> dict:
    (default, profiles) = process_yaml(text)
    if profile_name:
        profile = profiles[profile_name]
    elif default:
        profile = profiles[default]
    else:
        raise Exception('Error: No profile specified and no default defined.')
        # FIXME maybe throw an Except.
    return profile
    

def get_profile_from_file(filepath: str, profile_name: str=None) -> dict:
    '''Provide a configuration profile from a file'''
    with open(filepath, 'r') as f:
        text = f.read()
    return get_profile(text, profile_name)


# from pprint import pprint
# pprint(profiles)
# pprint(default)

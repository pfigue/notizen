# coding: utf-8


import yaml
from pprint import pprint
from notizen import config


def test_flat_list1():
    text="""- animals:
        - elephant: dumbo
        - horse
        - fish:
            - salmon
            - tuna"""
    data = yaml.load(text)
    print(data)
    expected_result = {
        'animals': {
            'elephant': 'dumbo',
            'fish': {
                'salmon': None, 'tuna': None
                },
            'horse': None,
            },
        }
    r = config.flat_list(data)
    pprint(r)
    assert r == expected_result


def test_process_yaml():
    text = """- profile:
    - name: noti2
    - path: /path/to/noti2
    - engine:
        - name: pickle
        - file: /path/to/pickle

- default: noti2"""
    (d, ps) = config.process_yaml(text)
    assert d == 'noti2' and list(ps.keys()) == ['noti2',]


def test_get_profile1():
    """Check if get_profile returns a defined profile"""
    text = """- profile:
    - name: noti2
    - path: /path/to/noti2
    - engine:
        - name: pickle
        - file: /path/to/pickle

- default: noti2"""
    expected_result = {
        'engine': {
            'file': '/path/to/pickle',
            'name': 'pickle'
            },
        'name': 'noti2',
        'path': '/path/to/noti2',
        }

    r = config.get_profile(text, 'noti2')
    assert r == expected_result


def test_get_profile2():
    """Check if get_profile returns the default profile when not profile specified."""
    text = """- profile:
    - name: noti2
    - path: /path/to/noti2
    - engine:
        - name: pickle
        - file: /path/to/pickle

- default: noti2"""
    expected_result = {
        'engine': {
            'file': '/path/to/pickle',
            'name': 'pickle'
            },
        'name': 'noti2',
        'path': '/path/to/noti2',
        }
    r = config.get_profile(text)
    assert r == expected_result


def test_get_profile3():
    """Check if get_profile returns ... FIXME what?
    no profile is selected. there is no default profile.
    throw an error? return the profile is only one is defined?"""
    text = """- profile:
    - name: noti2
    - path: /path/to/noti2
    - engine:
        - name: pickle
        - file: /path/to/pickle"""
    expected_result = {
        'engine': {
            'file': '/path/to/pickle',
            'name': 'pickle'
            },
        'name': 'noti2',
        'path': '/path/to/noti2',
        }
    try:
        r = config.get_profile(text)
    except Exception as w:
        assert 1==1, "Exception rasied, everything good."
    else:
        assert 1==0, "Exception not raised!"
    # FIXME improve this exception check

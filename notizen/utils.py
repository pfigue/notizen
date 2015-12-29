# coding: utf-8


import pprint
import io


_CPRINT_BUFFER = io.StringIO()
_CPRINT_PP = pprint.PrettyPrinter(indent=4, stream=_CPRINT_BUFFER)


def cprint(v, prefix=None):
    ''' '''
    p1 = type(v)
    _CPRINT_BUFFER.seek(0)
    _CPRINT_BUFFER.truncate()
    _CPRINT_PP.pprint(v)
    p2 = _CPRINT_BUFFER.getvalue()
    p2 = p2.strip()  # Remove trailing \n
    msg = '{}: {}'
    if prefix:
        msg = '{} ' +  msg
        msg = msg.format(prefix, p1, p2)
    else:
        msg = '{}: {}'
        msg = msg.format(p1, p2)
    print(msg)

v = {'key': 1234}

cprint(v)
# pq.pprint(v)
# print(foo)
# print(foo.getvalue())
# #foo.write('abdc')
# #foo.flush()
# #print(foo.getvalue())
w = (4, 5 , 3, )
cprint(w)
cprint(w)
# print(foo.getvalue())

# coding: utf-8


from notizen import utils


__BUFF_PATCHED_PRINT = None


def patched_print(msg: str):
	global __BUFF_PATCHED_PRINT
	__BUFF_PATCHED_PRINT = msg


def test_cprint(monkeypatch):
	v = {'key': 1234}
	monkeypatch.setattr('builtins.print', patched_print)
	utils.cprint(v)
	assert __BUFF_PATCHED_PRINT == '<class \'dict\'>: {\'key\': 1234}'
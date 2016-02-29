"""
Goal is to receive something like

{
	'path': '/path/to/notizen/',
	'engine': notizen.indexing.pickle',
	'engine_params': {
		'file': '/path/to/file',
	}
}

or:

{
	'engine': notizen.indexing.elastic',
	'engine_params': {
		'host': '/path/to/file',
		'port': 9200,
		'index_name': 'notizen',  # i think 1 index is ok.
	},
}

After having...:
	1. set default values:
		{
			'config_file': '~/.config/notizen/notizen.ini'
		}
	2. trying to read the provided file
		1. Callback to validate the file can be read. (read 1 byte and it is ok if there is no exception).
		2. 

"""

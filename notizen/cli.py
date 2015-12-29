#!/usr/bin/env python3
# coding: utf-8
'''
Command-line Interface to index and to search into the notes.
'''

import os
import click
import logging
from os import path
from clickclick import AliasedGroup

import notizen
from notizen import indices
from notizen.updatedb import update_tags_index
from notizen import config
from notizen import utils


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
CONFIG_DIR_PATH = click.get_app_dir('notizen')
INDICES_FILE_PATH = path.join(CONFIG_DIR_PATH, 'indices.pickle')
PROFILES_FILE_PATH = path.join(CONFIG_DIR_PATH, 'profile.yaml')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_COMMAND = 'test_default'


class AliasedDefaultGroup(AliasedGroup):

    def resolve_command(self, ctx, args):
        cmd_name = args[0]
        cmd = AliasedGroup.get_command(self, ctx, cmd_name)
        if not cmd:
            cmd_name = DEFAULT_COMMAND
            cmd = AliasedGroup.get_command(self, ctx, cmd_name)
            new_args = args
        else:
            new_args = args[1:]
        return cmd_name, cmd, new_args


def print_version(ctx, param, value):
    '''Shows the --version banner.
    With additional info in case of someone wants to report a bug.'''
    if not value or ctx.resilient_parsing:
        return

    msg = u'''{1} version {0}
{3}

Distributed under {4} license.
Authors: {5}.
{6}
Platform: '{2}'.'''

    args = (notizen.__version__, notizen.__program_name__,
            notizen.get_platform_id(), notizen.__short_description__,
            notizen.__license__, ', '.join(notizen.__authors__),
            notizen.__url__)

    msg = msg.format(*args)
    click.echo(msg)
    ctx.exit()


@click.group(cls=AliasedDefaultGroup, context_settings=CONTEXT_SETTINGS)
# FIXME click.version_option instead of this:
@click.option('-V', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
@click.pass_context
def cli(context):
    # FIXME what to do here?
    # context.obj = config_file
    pass


@cli.command('updatedb')
@click.option('--config-path', default=PROFILES_FILE_PATH,
    help='Path to the configuration file.', type=str)  # FIXME is there a filepath type?
@click.option('--index-path', default=None,
        help='Path to the index file.', type=str)
@click.argument('path')
@click.pass_obj
def updatedb(obj, config_path: str, index_path: str, path: str) -> None:
    '''Command to index all the notes with their tags.'''

    profile = config.get_profile_from_file(config_path, profile_name=None)  # FIXME improve error messsage when FileNotFoundError
    utils.cprint(profile)
    engine = profile['engine']['name']
    if engine == 'pickle':
        if index_path is None:  # If not provided in the CLI,
            index_path = profile['engine']['file']  # then take it.
    if index_path is None:  # If still not defined, set default.
        index_path = INDICES_FILE_PATH

    utils.cprint(index_path)

    (tags_index, ) = ({}, )
    update_tags_index(tags_index, path)

    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)
    indices.save_indices(tags_index, index_path)


@cli.command('locate')
@click.option('--config-path', default=PROFILES_FILE_PATH,
    help='Path to the configuration file.', type=str)  # FIXME is there a filepath type?
@click.option('--index-path', default=None,
        help='Path to the index file.', type=str)
@click.argument('tag')
@click.pass_obj
def locate(obj, config_path: str, index_path: str, tag: str) -> None:
    '''Show matching files with the given :tag.'''

    profile = config.get_profile_from_file(config_path, profile_name=None)  # FIXME improve error messsage when FileNotFoundError
    utils.cprint(profile)
    engine = profile['engine']['name']
    if engine == 'pickle':
        if index_path is None:  # If not provided in the CLI,
            index_path = profile['engine']['file']  # then take it.
    if index_path is None:  # If still not defined, set default.
        index_path = INDICES_FILE_PATH

    utils.cprint(index_path)

    (tags_index, ) = indices.load_indices(index_path)

    matching_files = tags_index.get(tag, None)
    if matching_files is None:
        msg = 'No matching files with "{}" tag.\n\nMisspelled? or inexistent?'
        msg = msg.format(tag)
        print(msg)
        return  # FIXME return error to shell
        # obj.exit(1)?

    msg = '{} matching files under tag "{}":'
    print(msg.format(len(matching_files), tag))
    for f in matching_files:
        print('\t{}'.format(f))


def main():
    cli()


if __name__ == '__main__':
    main()

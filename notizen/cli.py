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


from notizen import (config, utils, engines, helpers)


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# FIXME move this to a notize.config.defaults module?
CONFIG_DIR_PATH = click.get_app_dir('notizen')
INDICES_FILE_PATH = path.join(CONFIG_DIR_PATH, 'indices.pickle')
PROFILES_FILE_PATH = path.join(CONFIG_DIR_PATH, 'profile.yaml')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_COMMAND = 'test_default'


config_path_option = click.option('--config-path', default=PROFILES_FILE_PATH,
    help='Path to the configuration file.', type=click.Path(exists=True))
profile_name_option = click.option('--profile-name', default=None,
    help='Profile to use.', type=str)  # FIXME should be optional.


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


@cli.command()
@config_path_option
@profile_name_option
@click.argument('path')  # FIXME ideally it should be in the profile.
@click.pass_obj
def updatedb(obj, config_path: str, profile_name: str, path: str) -> None:
    '''Command to index all the notes with their tags.'''

    profile = config.get_profile_from_file(config_path, profile_name=profile_name)  # FIXME improve error messsage when FileNotFoundError
    ng = engines.get_engine(profile)
    helpers.walk_and_index(path, ng.index_doc)
    ng.shutdown()


@cli.command()
@config_path_option
@profile_name_option
@click.argument('tag')
@click.pass_obj
def locate(obj, config_path: str, profile_name: str, tag: str) -> None:
    '''Show matching files with the given :tag.'''

    profile = config.get_profile_from_file(config_path, profile_name=profile_name)  # FIXME improve error messsage when FileNotFoundError
    ng = engines.get_engine(profile)

    # Search and print results.
    matching_files = ng.search_by_tags(tag)
    helpers.show_matching_files(matching_files, tag)
    ng.shutdown()


def main():
    cli()


if __name__ == '__main__':
    main()

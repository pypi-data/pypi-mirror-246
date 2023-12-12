"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.

License: MIT

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

# Standard deps
import argparse
from pathlib import Path
from typing import Any, Optional

# Third-party deps
import rich.traceback
rich.traceback.install(show_locals=True, suppress=[rich])

# Local deps
import archadeptcli
from archadeptcli.console import getConsole, RichAlign, RichGroup, RichPanel
from archadeptcli.docker import DockerCLIWrapper
from archadeptcli.exceptions import *

class CommandLineArgs():
    """ Class representing the arguments parsed from the command line. """

    def __init__(self):
        """ Parse command line arguments. """

        # Data-driven description which we use at runtime to programmatically
        # generate the various argument parsers. This also lets us share flags
        # and arguments between commands without duplicated code/logic.
        args_descr = {
            'commands': (
                {
                    'command': 'make',
                    'dict': {
                        'help': 'invoke project Makefile',
                        'description': 'Invokes an ArchAdept example project Makefile.',
                    },
                },
                {
                    'command': 'run',
                    'dict': {
                        'help': 'run project on simulated hardware',
                        'description': 'Runs an ArchAdept example project on a simulated Raspberry Pi 3b.',
                    },
                },
                {
                    'command': 'debug',
                    'dict': {
                        'help': 'attach debugger to live simulation',
                        'description': 'Attaches a GDB debug session to a live QEMU simulation started by `archadept run`.',
                    },
                },
                {
                    'command': 'prune',
                    'dict': {
                        'help': 'clean up any lingering Docker containers',
                        'description': 'Cleans up any lingering Docker containers from previous ArchAdept CLI invocations.',
                    },
                },
            ),
            'args': (
                {
                    'arg': '-D',
                    'top-level': True,
                    'dict': {
                        'dest': 'debug',
                        'help': 'enable logging debug messages',
                        'action': 'store_true',
                    },
                },
                {
                    'arg': '-p',
                    'top-level': False,
                    'commands': ('make', 'run'),
                    'dict': {
                        'metavar': 'PROJECT',
                        'dest': 'workdir',
                        'help': 'path to the ArchAdept project (default: current directory)',
                        'type': Path,
                        'default': Path.cwd(),
                    },
                },
                {
                    'arg': '-i',
                    'top-level': False,
                    'commands': ('make', 'run'),
                    'dict': {
                        'metavar': 'IMAGE',
                        'dest': 'image',
                        'help': 'override Docker image repository (default: archadept/example-code-tools)',
                        'type': str,
                        'default': 'archadept/example-code-tools',
                    },
                },
                {
                    'arg': '-t',
                    'top-level': False,
                    'commands': ('make', 'run'),
                    'dict': {
                        'metavar': 'TAG',
                        'dest': 'tag',
                        'help': 'override Docker image tag (default: latest)',
                        'type': str,
                        'default': 'latest',
                    },
                },
                {
                    'arg': '-s',
                    'top-level': False,
                    'commands': ('run', ),
                    'dict': {
                        'dest': 'spawn_gdbserver',
                        'help': 'spawn GDB debug server and pause simulation at kernel entrypoint',
                        'action': 'store_true',
                    },
                },
                {
                    'arg': 'target',
                    'top-level': False,
                    'commands': ('make', ),
                    'dict': {
                        'metavar': 'TARGET',
                        'help': 'Makefile target from {all,clean,rebuild,dis,syms} (default: all)',
                        'type': str,
                        'choices': ('all', 'clean', 'rebuild', 'dis', 'syms'),
                        'default': 'all',
                        'nargs': '?',
                    },
                },
                {
                    'arg': 'container_id',
                    'top-level': False,
                    'commands': ('debug', ),
                    'dict': {
                        'metavar': 'CONTAINER',
                        'help': 'container in which the QEMU simulation is running, as given by `archadept run`',
                        'type': str,
                    },
                },
            ),
        }

        parser = argparse.ArgumentParser(prog='archadept')
        subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

        # Tracks argument parsers and command-specific argument groups associated
        # with each command's help screen.
        m_subparsers = dict()
        m_groups = dict()
        for command in args_descr['commands']:
            subparser = subparsers.add_parser(command['command'], **command['dict'])
            m_subparsers[command['command']] = subparser
            if command['command'] not in m_groups:
                m_groups[command['command']] = dict()
            m_groups[command['command']]['flags'] = subparser.add_argument_group('command-specific options')
            m_groups[command['command']]['positionals'] = subparser.add_argument_group('command-specific positional arguments')

        # Programmatically add each arg to its associated commands.
        for arg in args_descr['args']:
            # We first need to build up a list of "target" parsers to which we'll
            # be adding this arg. This determines whether the arg appears for a
            # particular command's help screen, and in which section it appears.
            targets = []
            if 'top-level' in arg and arg['top-level']:
                # Common options section of all parsers.
                targets.append(parser)
                targets += [m_subparsers[command['command']] for command in args_descr['commands']]
            elif arg['arg'].startswith('-'):
                # Command-specific flags section of the specified commands.
                targets += [m_groups[command]['flags'] for command in arg['commands']]
            else:
                # Command-specific positionals section of the specified commands.
                targets += [m_groups[command]['positionals'] for command in arg['commands']]
            # Now simply add the arg to each target identified above.
            for target in targets:
                target.add_argument(arg['arg'], **arg['dict'])

        # Parse the args into this CommandLineArgs object.
        for k,v in vars(parser.parse_args()).items():
            if k == 'workdir' and not Path(v).is_absolute():
                v = Path(Path.cwd(), v)
            setattr(self, k, v)

def main_make(image:str, tag:str, workdir:Path, target:str) -> int:
    """ Main function for ``archadept make``.

    Parameters
    ----------
    image
        Docker image repository to use.
    tag
        Docker image tag to use.
    workdir
        Path to the ArchAdept example project.
    target
        Makefile target.

    Returns
    -------
    Shell exit status of the underlying ``make`` invocation.
    """
    result = DockerCLIWrapper().run(f'make {target}', image=image, tag=tag, host_workdir=workdir)
    return result.returncode

def main_run(image:str, tag:str, workdir:Path, spawn_gdbserver:bool) -> int:
    """ Main function for ``archadept run``.

    Parameters
    ----------
    image
        Docker image repository to use.
    tag
        Docker image tag to use.
    workdir
        Path to the ArchAdept example project.
    spawn_gdbserver
        Whether to spawn a GDB server and pause simulation at kernel entrypoint.

    Returns
    -------
    Shell exit status of the underlying QEMU simulation.
    """
    console = getConsole()
    docker = DockerCLIWrapper()
    qemu_cmdline = f'qemu-system-aarch64 -M raspi3b -nographic -kernel build/out.elf'
    if spawn_gdbserver:
        qemu_cmdline += ' -s -S'
    result = docker.run(qemu_cmdline, detached=True, image=image, tag=tag, host_workdir=workdir)
    if result.returncode != 0:
        docker.error_cli_result(result)
        raise SimulationError('failed to start QEMU simulation')
    container_id = result.output
    if len(container_id) > 16:
        container_id = container_id[:16]
    renderables = []
    if spawn_gdbserver:
        renderables.append('Simulation is paused waiting for debugger.\n' \
                               'Run this command in another window to attach the debugger:')
        debug_panel = RichPanel.fit(f'$ archadept debug {container_id}', style='blue')
        renderables.append(RichAlign.center(debug_panel))
    renderables.append('Press \'Ctrl-a\' followed by \'x\' to end the simulation.\n' \
                       'QEMU is now controlling this terminal window until the simulation ends...')
    console.print(RichPanel.fit(RichGroup(*renderables), style='green'))
    return docker.attach(container_id).returncode

def main_debug(container_id:str) -> int:
    """ Main function for ``archadept debug``.

    Parameters
    ----------
    container_id
        ID of the container in which the QEMU simulation is running.

    Returns
    -------
    Shell exit status of the underlying GDB invocation.
    """
    gdb_command = 'aarch64-none-elf-gdb -q -ex \'target remote localhost:1234\' build/out.elf'
    return DockerCLIWrapper().exec(container_id, gdb_command).returncode

def main_prune() -> int:
    """ Main function for ``archadept prune``.

    Returns
    -------
    Shell exit status of the underlying sequence of calls to the Docker CLI.
    """
    DockerCLIWrapper().prune()
    return 0

def main():
    """ Main entrypoint function when invoked from the command line. """
    args = CommandLineArgs()
    archadeptcli.console.init(debug=args.debug)
    try:
        if args.command == 'make':
            return main_make(args.image, args.tag, args.workdir, args.target)
        elif args.command == 'run':
            return main_run(args.image, args.tag, args.workdir, args.spawn_gdbserver)
        elif args.command == 'debug':
            return main_debug(args.container_id)
        elif args.command == 'prune':
            return main_prune()
        else:
            raise InternalError(f'unimplemented function: main_{args.command}()')
    except ArchAdeptError as e:
        if args.debug:
            raise e
        else:
            getConsole().print(e)
            return 1
    except Exception as e:
        raise UngracefulExit('crashed due to uncaught exception') from e


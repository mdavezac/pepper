#! {{condiment_python}}
import click
import setup

DEFAULT_PREFIX = setup.DEFAULT_PREFIX


def _options(prefix=DEFAULT_PREFIX):
    from py.path import local
    return str(local(prefix).join('build', 'etc', 'salt', 'minion'))


@click.group()
def cli():
    pass

cli.add_command(setup.cli, 'setup')


def _get_compiler(prefix, compiler):
    if compiler is not None and len(compiler) > 0:
        return compiler
    result = setup.get_pillar(prefix, 'compiler')['compiler']
    if len(result) > 0:
        return result
    return "gcc"


def _get_python(prefix, python):
    if python is not None and len(python) > 0:
        return python
    result = setup.get_pillar(prefix, 'python')['python']
    if len(result) > 0:
        return result
    return "python3"


def _get_mpi(prefix, mpi):
    if mpi is not None and len(mpi) > 0:
        return mpi
    result = setup.get_pillar(prefix, 'mpi')['mpi']
    if len(result) > 0:
        return result
    return "openmpi"


def _get_pillar(prefix, compiler, python, mpi):
    return {'compiler': _get_compiler(prefix, compiler),
            'python': _get_python(prefix, python),
            'mpi': _get_mpi(prefix, mpi)}


@cli.command(help="Run a given state, or all states if none given")
@click.option('--prefix', default=DEFAULT_PREFIX, type=click.Path(), nargs=1)
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
@click.option('--mpi', default=None, type=str, nargs=1,
              help="Default mpi")
@click.option('--verbose', is_flag=True, help="Verbose output")
@click.argument('states', nargs=-1)
def run(prefix, states, python, compiler, mpi, verbose):
    pillars = _get_pillar(prefix, compiler, python, mpi)
    setup.run_command(prefix, 'state.apply', *states,
                      pillar=pillars, minimize=not verbose)


@cli.command(help="Make a call to salt")
@click.argument('call', nargs=-1)
@click.option('--prefix', default=DEFAULT_PREFIX, type=click.Path())
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
@click.option('--mpi', default=None, type=str, nargs=1,
              help="Default mpi")
def call(prefix, call, python, compiler, mpi):
    assert len(call) >= 1
    pillars = _get_pillar(prefix, compiler, python, mpi)
    setup.run_command(prefix, *call, pillar=pillars, minimize=False)


@cli.command(help="Make a raw call to salt")
@click.option('--prefix', default=DEFAULT_PREFIX, type=click.Path())
@click.argument('call', nargs=-1)
def rawcall(prefix, call):
    assert len(call) >= 1
    setup.run_command(prefix, *call, minimize=False)


@cli.command(help="Show a (the) given state(s) in yaml format")
@click.argument('states', nargs=-1)
@click.option('--prefix', default=DEFAULT_PREFIX, type=click.Path())
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
@click.option('--mpi', default=None, type=str, nargs=1,
              help="Default mpi")
def show(states, prefix, compiler, python, mpi):
    pillars = _get_pillar(prefix, compiler, python, mpi)
    setup.run_command(prefix, 'state.show_sls', *states,
                      pillar=pillars, minimize=False)


@cli.command(help="Update to latest CondimentStation")
@click.argument('prefix', default=DEFAULT_PREFIX, type=click.Path(), nargs=1)
def update(prefix):
    setup.run_command(prefix, 'state.apply',
                      'condiment_scripts', minimize=True)
    setup.run_command(prefix, 'saltutil.sync_all', minimize=False)
    setup.run_command(prefix, 'state.apply', 'salt', 'condiments', 'spack', 'funwith',
                      'black-garlic', minimize=True)


if __name__ == '__main__':
    cli()

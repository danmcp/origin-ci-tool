import click
from cli.prepare.isolated_install_options import isolated_install_options
from cli.prepare.playbooks_util import playbook_path
from cli.util.common_options import ansible_verbosity_option
from cli.util.preset_option import Preset
from util.playbook_runner import PlaybookRunner


def install_docker_for_preset(ctx, param, value):
    """
    Install Docker on the remote host for a given OpenShift version.
    Handles the special `--for` option.

    :param value: version of OpenShift for which to install Docker
    """
    if not value or ctx.resilient_parsing:
        return

    install_docker(version=docker_version_for_preset(value))
    ctx.exit()


def docker_version_for_preset(preset):
    """
    Determine the Docker version for a given preset.

    :param preset: version of OpenShift for which to install Docker
    :return: the Docker version to install
    """
    if preset in [Preset.origin_master, Preset.ose_master, Preset.ose_33, Preset.ose_321]:
        return '1.10.3'
    if preset in [Preset.ose_32]:
        return '1.9.1'
    else:
        raise click.UsageError('No Docker preset found for OpenShift version: %s' % preset)


@click.command(
    short_help='Install Docker on remote hosts.',
    help='''
Installs the Docker daemon and CLI on the remote host.

The Docker install can be parameterized with the Docker package
version that is required, as well as the existing RPM repositories
and new RPM repositories from the web to enable when installing it.

If repositories or repository URLs are given, they will be the only
repositories enabled when the Docker install occurs. Any repositories
created from repository URLs will be registered only for the Docker
install and will be removed after the fact.

If a preset is chosen, default values for the other options are used
and user-provided options are ignored.

\b
Examples:
  Install Docker for a specific version of OpenShift
  $ oct prepare docker --for=ose/enterprise-3.3
\b
  Install a specific Docker version present in default RPM repositories
  $ oct prepare docker --version=1.9.1
\b
  Install a specific Docker version from an available custom RPM repository
  $ oct prepare docker --version=1.10.3 --repo=my-custom-docker-repo
\b
  Install a specific Docker version from an RPM repository available on the web
  $ oct prepare docker --version=1.11.0 --repourl=myrepo.com/docker/x86_64/
'''
)
@isolated_install_options(
    package_name='Docker',
    preset_callback=install_docker_for_preset
)
@ansible_verbosity_option
def docker(version, repos, repourls, preset):
    """
    Installs the Docker daemon and CLI on the remote host.

    :param version: version of Docker to install
    :param repos: list of RPM repositories from which to install Docker
    :param repourls: list of RPM repository URLs from which to install Docker
    :param preset: version of OpenShift for which to install Docker
    """
    install_docker(version, repos, repourls)


def install_docker(version, repos=None, repourls=None):
    """
    Install Docker on the remote host.

    :param version: version of Docker to install
    :param repos: list of RPM repositories from which to install Docker
    :param repourls: list of RPM repository URLs from which to install Docker
    """
    vars = dict(
        origin_ci_docker_package='docker'
    )

    if version:
        vars['origin_ci_docker_package'] += '-' + version

    if repos:
        vars['origin_ci_docker_disabledrepos'] = '*'
        vars['origin_ci_docker_enabledrepos'] = ','.join(repos)

    if repourls:
        vars['origin_ci_docker_tmp_repourls'] = repourls

    PlaybookRunner().run(
        playbook_source=playbook_path('docker'),
        vars=vars
    )
"""Implementations used to safely kill a running battle, cleaning up possibly running docker containers."""
import signal
import sys
import logging
import subprocess
import os

logger = logging.getLogger('algobattle.sighandler')


def signal_handler(sig, frame):
    """Handle interrupts and exit the process gracefully."""
    _kill_spawned_docker_containers()

    logger.info('Received SIGINT, terminating execution.')
    os.killpg(os.getpid(), signal.SIGTERM)

    sys.exit(0)


def _kill_spawned_docker_containers():
    """Terminate all running docker containers spawned by this program."""
    if latest_running_docker_image:
        subprocess.run('docker ps -a -q --filter ancestor={} | xargs -r docker kill > /dev/null 2>&1'
                       .format(latest_running_docker_image), shell=True)


signal.signal(signal.SIGINT, signal_handler)
latest_running_docker_image = ""

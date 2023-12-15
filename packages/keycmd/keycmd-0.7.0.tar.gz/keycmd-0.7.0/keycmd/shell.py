import os
from pathlib import Path
from pprint import pformat
from subprocess import run
from sys import exit

from shellingham import ShellDetectionFailure, detect_shell

from .logs import vlog, vwarn

USE_SUBPROCESS = False  # exposed for testing
IS_WINDOWS = os.name == "nt"
IS_POSIX = os.name == "posix"


def exec(args, env):
    if USE_SUBPROCESS or IS_WINDOWS:
        # windows does not support process replacement
        # as well as posix systems do
        p = run(args, shell=False, env=env)
        exit(p.returncode)
    # i know this looks like a bug
    # but it's a mandatory convention
    # to pass the process name as the first argument
    os.execvpe(args[0], args, env)


def get_shell():
    """Use shellingham to detect the shell that invoked
    this Python process"""
    try:
        shell_name, shell_path = detect_shell(os.getpid())
    except ShellDetectionFailure:
        vwarn("failed to detect parent process shell, falling back to system default")
        if IS_POSIX:
            shell_path = os.environ["SHELL"]
        elif IS_WINDOWS:
            shell_path = os.environ["COMSPEC"]
        else:
            raise NotImplementedError(f"os {os.name} support not available")
        shell_name = Path(shell_path).name.lower()
    vlog(f"detected shell: {shell_path}")
    return shell_name, shell_path


def run_shell(env=None):
    """Open an interactive shell for the user to interact
    with."""
    shell_name, shell_path = get_shell()
    vlog(f"spawning subshell: {shell_name}")
    exec([shell_path], env)


def run_cmd(cmd, env=None):
    """Run a one-off command in a shell."""
    shell_name, shell_path = get_shell()
    if shell_name == "cmd":
        opt = "/C"
    else:
        opt = "-c"
        cmd = [" ".join(cmd)]
    full_command = [shell_path, opt, *cmd]
    vlog(f"running command: {pformat(full_command)}")
    exec(full_command, env)

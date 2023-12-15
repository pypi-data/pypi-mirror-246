"""Command line tool to find and gather system information."""

__version__ = "0.0.1"
import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple, List

SYFT_PATHS = ["/usr/bin/syft", Path.home() / "bin/syft", "/usr/local/bin/syft"]
DPKG_PATH = "/var/lib/dpkg"
SYFT_PATH = "/usr/bin/syft"
RPM_PATH = "/var/lib/rpm"


def system(cmd) -> Tuple[bytes, bytes, int]:
    """
    Invoke a shell command.
    :returns: A tuple of output, err message in bytes and return code.
    """
    ret = subprocess.Popen(
        cmd,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    out, err = ret.communicate()
    return out, err, ret.returncode


def find_syft():
    "Returns the path to the syft binary."
    for sp in SYFT_PATHS:
        if os.path.exists(sp):
            return sp
    else:
        return ""


def generate_syft_command(path: str, filename: str, hostname: str) -> List[str]:
    "Returns the command to execute."
    command = [SYFT_PATH, path, "-o" f"spdx-json={filename}", "--source-name", hostname]
    return command


def main():
    "Command line entry point."
    parser = argparse.ArgumentParser(prog="hittade", description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()

    # First check if the syft binary is available
    global SYFT_PATH
    SYFT_PATH = find_syft()
    if not SYFT_PATH:
        print("Could not find syft binary at the system.", file=sys.stderr)
        sys.exit(1)
    hostname = subprocess.check_output(["/usr/bin/hostname", "--fqdn"]).decode("utf-8").strip()
    if not hostname:
        hostname = "default-host"

    # If DPKG_PATH is available, scan it
    if os.path.exists(DPKG_PATH):
        cmd = generate_syft_command(DPKG_PATH, "server.spdx.json", hostname)
    elif os.path.exists(RPM_PATH):
        cmd = generate_syft_command(RPM_PATH, "server.spdx.json", hostname)

    _out, _err, retcode = system(cmd)
    if retcode != 0:
        print(f"Failed to generate server spdx-json for {hostname}", file=sys.stderr)
        sys.exit(retcode)


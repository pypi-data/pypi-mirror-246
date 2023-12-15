# hittade

A command line tool to find and gather system information. This tools submits the information to the corresponding web application. It uses [syft](https://github.com/anchore/syft) inside to generate the actual SBOM files.


## Setup for development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
flit install --symlink
```

## Usage

```
hittade --help
usage: hittade [-h] [-v]

Command line tool to find and gather system information.

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```


## LICENSE: BSD-2-Clause
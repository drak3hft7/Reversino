# Reversino

![02](images/02.png 'Banner')

Reversino is a Python tool for finding subdomains from IP ranges or CIDR subnets. It uses the Reverse DNS Lookup method, which involves performing a reverse DNS lookup on each IP within the range. This technique attempts to resolve each IP address to an associated domain name.

## Installation

```bash

```

## Usage:
```bash
python3 Reversino.py -h
```
- `--help` or `-h` show this help message and exit.
- `--file` or `-f` Path to te file containing IP ranges (format: start-end) or CIDR (e.g., 195.49.41.0/24).
- `--all` or `-a`  Use this option if the file contains both IP ranges and CIDR subnets.

![01](images/01.png 'Help')

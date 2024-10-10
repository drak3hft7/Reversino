# Reversino

![02](images/02.png 'Banner')

Reversino is a Python tool for finding subdomains from IP ranges or CIDR subnets. It uses the Reverse DNS Lookup method, which involves performing a reverse DNS lookup on each IP within the range. This technique attempts to resolve each IP address to an associated domain name.

Last update: **10 Oct 2024**

- 10 Oct 2024: Now Reversino supports integration with Discord via webhook to receive notifications in your channel.

## Installation

```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 Reversino.py -h
```
- `--help` or `-h` show this help message and exit.
- `--file` or `-f` Path to te file containing IP ranges (format: start-end) or CIDR (e.g., 195.49.41.0/24).
- `--all` or `-a`  Use this option if the file contains both IP ranges and CIDR subnets.

![01](images/01.png 'Help')

### Example with a file containing both IP ranges and CIDR subnets

Contents of the file range_all.txt:
```
173.0.84.0/28
173.0.84.190-173.0.84.200
```

Usage:
```bash
python3 Reversino.py -f range_all.txt -a
```

![03](images/03.png 'All')

### Example with a file containing IP ranges (format: start-end)

Contents of the file range_start-end.txt:
```
173.0.84.190-173.0.84.200
```

Usage:
```bash
python3 Reversino.py -f range_start-end.txt
```

![04](images/04.png 'All')

### Example with a file containing CIDR (e.g., 195.49.41.0/24)

Contents of the file range_cidr.txt:
```
173.0.84.0/28
```

Usage:
```bash
python3 Reversino.py -f range_cidr.txt
```

![05](images/05.png 'All')

## Notifications in your Discord channel through a webhook.

By creating a webhook endpoint on your Discord server, you will generate a webhook URL that you can insert into the source code to receive notifications.

![07](images/07.png 'All')

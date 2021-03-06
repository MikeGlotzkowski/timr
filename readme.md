# Time to submit while mobile working ヽ(´▽`)/

## Setup (currently)

```bash
# first time
python3 -m venv env
source ./env/bin/activate
python3 -m pip install -r requirements.txt
(env) user@work:~/dev/timr$ python3 src/timr.py --help
Usage: timr.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  calc
  configure
  version
```

## Short Docu

### calculate work time

```bash
Usage: timr.py calc [OPTIONS]

Options:
  -s, --start-time TEXT
  -e, --end-time TEXT
  -b, --break-time TEXT
  -ch, --contract-hours-per-day TEXT
  --local-config / --no-local-config
  --help
```

### configure defaults

```bash
Usage: timr.py configure [OPTIONS]

Options:
  --start-time TEXT              [required]
  --end-time TEXT                [required]
  --break-time TEXT              [required]
  --contract-hours-per-day TEXT  [required]
  --help                         Show this message and exit.
```

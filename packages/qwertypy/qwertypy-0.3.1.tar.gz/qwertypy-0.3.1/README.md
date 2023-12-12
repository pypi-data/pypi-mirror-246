# qwertypy

My personal utilities library.

## Virtual Environment

```bash
# Create new venv
py -m venv ./venv

# Activate venv
## In Windows git bash
source ./venv/Scrips/activate
```

To See which venv:

```py
import sys

print(sys.prefix)
```

Install required packages

```bash
pip install -r requirements.txt
```

## Testing

```bash
py -m unittest
```

## Release

### Steps

1. Update `setup.py` with version no.
2. Update `CHANGELOG.md``.

```bash
py release.py
```

## Resources

### Setup and configurations

1. Project setup: https://medium.com/vlmedia-tech/step-by-step-guide-to-create-python-library-using-ci-cd-pipeline-8e66022108df
2. Changelog: https://keepachangelog.com/
3. Running tests: https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory

# ytho

Change Python's prompt with ease. Because `>>>` is boring.

## Installation

```bash
pip install ytho
```

## Usage

Define a file `.ytho.py` in your home directory, with a class `Prompt`.

This will define your prompt. For example:

```python
class Prompt:
    def __init__(self):
        self.counter = 0

    def prompt(self) -> tuple[str, str]:
        self.counter += 1
        ps1 = f"\033[1;32mIn [{self.counter}] \033[m: "
        # The ANSI codes take up 10 chars, remove those
        ps2 = " " * (len(ps1) - 10)
        return ps1, ps2
```

And now you have IPython's prompt. And you can do a lot more than that if you want!.

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests

## Type Checking

Run `mypy .`

## Create and upload a package to PyPI

Make sure to bump the version in `setup.cfg`.

Then run the following commands:

```bash
rm -rf build dist
python setup.py sdist bdist_wheel
```

Then upload it to PyPI using [twine](https://twine.readthedocs.io/en/latest/#installation):

```bash
twine upload dist/*
```

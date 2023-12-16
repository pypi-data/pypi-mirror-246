# acecord

An easy-to-use extension for the [Pycord](https://github.com/Pycord-Development/pycord) library with some utility functions.

### Note: Some examples are outdated

## Features

- Json parser
- [Wrapper](https://github.com/Cryxyemi/aiosqlite-wrapper) for the [aiosqlite](https://pypi.org/project/aiosqlite/) library
- Pre-made Embeds
- Pre-made on_ready event (can be disabled)
- Custom logger (can be disabled and log to file)

## Installing

Python 3.8 or higher is required.

You can install the latest release from [PyPI](https://pypi.org/project/acecord/) (Coming soon).

```sh
pip install acecord
```

You can also install the latest Dev version. Note the Dev version maybe have bugs and can be unstable
and requires [git](https://git-scm.com/downloads) to be installed.

```sh
pip install git+https://github.com/sqiuwsqjjsxsajisaj/acecord.git
```

## Useful Links

- [Pycord Docs](https://docs.pycord.dev/)
- [Changelog](https://github.com/sqiuwsqjjsxsajisaj/blob/main/Changelog.md)

## Example

```py
import acecord as mc
import discord


ace = ac.ace(
    token="token"
)

if __name__ == "__main__":
    ace.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    ace.load_subdir("commands")  # Load all cogs in the "commands" folder and all subfolders

    ace.run() # Start the acecord
```

**Note:** It's recommended to load the token from a [`.env`](https://pypi.org/project/python-dotenv/) file, from a [`json file`](https://docs.python.org/3/library/json.html) or a normal [`python file`](https://docs.python.org/3/tutorial/modules.html)
instead of hardcoding it.

## Contributing

I am always happy to receive contributions. Here is how to do it:

1. Fork this repository
2. Make changes
3. Create a pull request

You can also [create an issue](https://github.com/sqiuwsqjjsxsajisaj/acecord/issues/new) if you find any bugs.

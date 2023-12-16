[![skycord](https://skycord.readthedocs.io/en/latest/_static/skycord.png)](https://github.com/svtano/skycord3)

[![](https://img.shields.io/discord/1010915072694046794?label=discord&style=for-the-badge&logo=discord&color=5865F2&logoColor=white)](https://discord.gg/zfvbjTEzv6)
[![](https://img.shields.io/pypi/v/skycord.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/skycord/)
[![](https://img.shields.io/pypi/l/skycord?style=for-the-badge)](https://github.com/svtano/skycord3/blob/main/LICENSE)
[![](https://aschey.tech/tokei/github/tibue99/skycord?style=for-the-badge)](https://github.com/svtano/skycord3)

An easy-to-use extension for the [Pycord](https://github.com/Pycord-Development/pycord) library with some utility functions.

## ⚠️ Note
Please use this library with the [Pycord master branch](https://github.com/Pycord-Development/pycord).

## Features
- Easy cog loading
- Automatic error handling
- Error report webhooks
- Embed templates
- Beautiful ready event
- Custom logging
- Automated help command
- Datetime and file utilities
- Wrapper for [aiosqlite](https://github.com/omnilib/aiosqlite)

While this library can be installed with any Discord library, most features will only work with Pycord.

## Installing
Python 3.9 or higher is required.
```
pip install skycord
```
You can also install the latest version from GitHub. Note that this version may be unstable
and requires [git](https://git-scm.com/downloads) to be installed.
```
pip install git+https://github.com/svtano/skycord3
```
If you need the latest version in your `requirements.txt` file, you can add this line:
```
skycord @ git+https://github.com/svtano/skycord3
```

## Useful Links
- [Documentation](https://skycord.readthedocs.io/)
- [Getting started](https://skycord.readthedocs.io/en/latest/pages/getting_started.html)
- [PyPi](https://pypi.org/project/skycord/)
- [Pycord Docs](https://docs.pycord.dev/)

## Example
- For more examples, see the [example repository](https://github.com/svtano/skycord3_template)
or the [sample code](https://skycord.readthedocs.io/en/latest/examples/examples.html).

```py
import skycord
import discord

bot = skycord.Bot(
    intents=discord.Intents.default()
)

if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run("TOKEN")
```
**Note:** It's recommended to [load the token](https://guide.pycord.dev/getting-started/creating-your-first-bot#protecting-tokens) from a `.env` file instead of hardcoding it.
skycord can automatically load the token if a `TOKEN` variable is present in the `.env` file.

## Contributing
I am always happy to receive contributions. Here is how to do it:
1. Fork this repository
2. Make changes
3. Create a pull request

You can also [create an issue](https://github.com/svtano/skycord3/issues/new) if you find any bugs.

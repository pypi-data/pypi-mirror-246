

[![]()](https://discord.gg/zfvbjTEzv6)
[![]()](https://pypi.org/project/netcord/)
[![](https://img.shields.io/pypi/l/netcord?style=for-the-badge)](https://github.com/tibue99/netcord/blob/main/LICENSE)
[![]()](https://github.com/sqiuwsqjjsxsajisaj/Netcord)

An easy-to-use extension for [Discord.py](https://github.com/Rapptz/discord.py)
and [Pycord](https://github.com/Pycord-Development/pycord) with some utility functions.

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

## Installing
Python 3.9 or higher is required.
```
pip install netcord
```
You can also install the latest version from GitHub. Note that this version may be unstable
and requires [git](https://git-scm.com/downloads) to be installed.
```
pip install git+https://github.com/sqiuwsqjjsxsajisaj/Netcord.git
```
If you need the latest version in your `requirements.txt` file, you can add this line:
```
netcord @ git+https://github.com/sqiuwsqjjsxsajisaj/Netcord.git
```

## Useful Links
- [PyPi](https://pypi.org/project/netcord/)
- [Pycord Docs](https://docs.pycord.dev/)

## Examples
- **Note:** It's recommended to [load the token](https://guide.pycord.dev/getting-started/creating-your-first-bot#protecting-tokens) from a `.env` file instead of hardcoding it.
netCord can automatically load the token if a `TOKEN` variable is present in the `.env` file.

### Pycord
```py
import netcord
import discord

bot = netcord.Bot(
    intents=discord.Intents.default()
)

if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.net("TOKEN")
```

### Discord.py
```py
import asyncio
import discord
import netcord


class Bot(netcord.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def setup_hook(self):
        await super().setup_hook()
        await self.tree.sync()


async def main():
    async with Bot() as bot:
        bot.add_help_command()
        bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
        await bot.netstart("TOKEN")


if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing
I am always happy to receive contributions. Here is how to do it:
1. Fork this repository
2. Make changes
3. Create a pull request

You can also [join the server ](https://discord.gg/PcaDmJpyjX) if you find any bugs.

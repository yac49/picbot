import asyncio
import traceback
import aiohttp
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError
initial_extensions = ['cogs.preset','cogs.util']

BOT_PREFIX = '-'
intents = discord.Intents.all()
load_dotenv()

class DBot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix=BOT_PREFIX, case_insensitive=True, intents=intents)
        self.session: aiohttp.ClientSession = None
        self.bot_version = '0.0.1'

    async def on_ready(self)-> None:
        print(f'We have logged in as {self.user}')
        guilds = [guild.id for guild in self.guilds]
        print(f"The {self.user.name} bot is in {len(guilds)} Guilds.\nThe guilds ids list : {guilds}")
        await self.tree.sync()

    async def setup_hook(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()
        await self.load_cogs()
        await self.tree.sync()

    async def load_cogs(self) -> None:
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except (
                ExtensionNotFound,
                NoEntryPointError,
                ExtensionFailed,
            ):
                print(f'Failed to load extension {extension}')
                traceback.print_exc()
    async def start(self) -> None:
        return await super().start(os.getenv('DISCORD_TOKEN'), reconnect=True)

def run_bot() -> None:
    try:
        bot = DBot()
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        exit


if __name__ == '__main__':
    run_bot()

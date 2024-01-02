from bot import DBot
from discord.ext import commands
import discord
import sqlite3
import os
from urllib.parse import urlparse

def get_url_before_ex(url):
  parsed_url = urlparse(url)
  return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

class PreSet(commands.Cog):
    def __init__(self, bot: DBot) -> None:
        self.bot: DBot = bot
        self.conn, self.cursor = None, None


    async def dbcon(self):
        dbfolder = os.path.join(os.path.dirname(__file__), '../db')

        if not os.path.exists(dbfolder):
            os.makedirs(dbfolder)

        database_file = os.path.join(dbfolder, 'data.db')

        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        return conn, cursor

    async def guild_data(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS guild_data (
            guild_id INTEGER,
            guild_name TEXT,
            channel_id INTEGER PRIMARY KEY,
            channel_name TEXT
        )
        ''')
        self.conn.commit()
    async def user_data(self, guild_name):
        guild_name = guild_name.replace(" ", "_")
        guild_name=str(guild_name)
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {guild_name}_user_data (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            money INTEGER
        )
        ''')
        self.conn.commit()

    async def get_guild_id(self, guild_name):
        for guild in self.bot.guilds:
            if guild.name == guild_name:
                return guild.id
        return None

    async def get_channel_id(self, guild_id, channel_name, channel_type):
        guild = self.bot.get_guild(guild_id)
        if guild:
            if channel_type == "text":
                for channel in guild.text_channels:
                    if channel.name == channel_name:
                        return channel.id
            elif channel_type == "voice":
                for channel in guild.voice_channels:
                    if channel.name == channel_name:
                        return channel.id
        return None

    async def fetch_guild_channel_id(self, guild_name, channel_name, channel_type):
        guild_id = await self.get_guild_id(guild_name)
        if channel_type == "text":
            channel_id = await self.get_channel_id(guild_id, channel_name, channel_type)
        elif channel_type == "voice":
            channel_id = await self.get_channel_id(guild_id, channel_name, channel_type)
        else:
            channel_id = None

        if guild_id and channel_id:
            self.cursor.execute('''
            INSERT OR IGNORE INTO guild_data (guild_id, guild_name, channel_id, channel_name)
                            VALUES (?, ?, ?, ?)'''
            , (guild_id, guild_name, channel_id, channel_name))
            self.conn.commit()
        else:
            print(f"Channel not found in {guild_name}")
            return guild_id, channel_id

    async def get_user_id(self,guild_name):
        members = self.bot.get_all_members() 
        for member in members:
            guild_name = guild_name.replace(" ", "_")
            guild_name=str(guild_name)
            self.cursor.execute(f'''
            INSERT OR IGNORE INTO {guild_name}_user_data (user_id, user_name, money)
                            VALUES (?, ?, ?)'''
            , (member.id, str(member.name), 0))

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.guild_data()


            for guild in self.bot.guilds:
                await self.user_data(guild.name)
                await self.get_user_id(guild.name)
                for channel in guild.text_channels:
                    try:
                        await self.fetch_guild_channel_id(guild.name, channel.name, channel_type="text")
                        try:
                            async for message in channel.history(limit=100):
                                for attachment in message.attachments:
                                    if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                                        dbfolder = os.path.join(os.path.dirname(__file__), '../db')

                                        if not os.path.exists(dbfolder):
                                            os.makedirs(dbfolder)

                                        database_file = os.path.join(dbfolder, 'pic_data.db')

                                        conn = sqlite3.connect(database_file)
                                        cursor = conn.cursor()
                                        guild_name = message.guild.name.replace(" ", "_")
                                        cursor.execute(f'''
                                            CREATE TABLE IF NOT EXISTS {guild_name}_pics (
                                                name TEXT,
                                                channel TEXT,
                                                jump TEXT,
                                                img TEXT UNIQUE
                                            )
                                        ''')

                                        url_before_ex = get_url_before_ex(attachment.url)
                                        cursor.execute(f"SELECT * FROM {guild_name}_pics WHERE img LIKE ?", (f"{url_before_ex}%",))
                                        existing_row = cursor.fetchone()


                                        if existing_row is None:
                                            cursor.execute(f'''
                                                INSERT INTO {guild_name}_pics (name, channel, jump, img)
                                                VALUES (?, ?, ?, ?)
                                            ''', (message.author.name, channel.name, message.jump_url, attachment.url))
                                        cursor.execute(f'''
                                            INSERT OR IGNORE INTO {guild_name}_pics (name, channel, jump, img)
                                            VALUES (?, ?, ?, ?)
                                        ''', (message.author.name, channel.name, message.jump_url, attachment.url))
                                        conn.commit()
                                        conn.close()
                        except discord.Forbidden:
                                continue
                        await self.fetch_guild_channel_id(guild.name, channel.name, channel_type="text")
                    except Exception as e:
                        print(f"Error fetching guild and channel ID for {guild.name} {channel.name}: {e}")
                for channel in guild.voice_channels:
                    try:
                        await self.fetch_guild_channel_id(guild.name, channel.name, channel_type="voice")
                    except Exception as e:
                        print(f"Error fetching guild and channel ID for {guild.name} {channel.name}: {e}")
        except Exception as e:
            print(e)
        print('Preset is ready')

async def setup(bot: DBot) -> None:
    cog = PreSet(bot)
    cog.conn, cog.cursor = await cog.dbcon()
    await bot.add_cog(cog)

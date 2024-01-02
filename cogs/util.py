import asyncio
from datetime import datetime, time, timedelta
import random
import discord
import sqlite3
import os
from discord.ext import commands,tasks
from discord import app_commands
from utils.dad_joke import dad
from utils.pic import store_pics,get_pics,PicView
from utils.nba import NBAView,ifPistonWin
from utils.chat import input_response
from bot import DBot
from urllib.parse import unquote



class util(commands.Cog, name='utility'):
    def __init__(self, bot: DBot) -> None:
      self.bot: DBot = bot
      self.pistons_game_title=""
      self.pistons_strike=0
      self.statusloop.start() 
   
    @app_commands.command(name='pictures',
              description="看看這裡有什麼照片@@")
    async def pic_command(self,interaction: discord.Interaction):
      try:
        view = PicView(interaction, get_pics(interaction.guild.name.replace(" ", "_"),interaction.channel.name)) 
        await view.show_embed()
      except:
        embed = discord.Embed(description="這裡沒有照片@@")
        await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(name="joke",description="講一個不好笑的工程師笑話ˋˊ")
    async def joke_command(self,interaction: discord.Interaction):
        joke=dad()
        await interaction.response.send_message(embed=joke)

    @app_commands.command(name="nba", description="看看今天NBA的比數")
    async def nba_command(self, interaction: discord.Interaction):
        try:
            game = NBAView(interaction)
            await interaction.response.defer()
        except Exception as e:
            print(e)
        if game:
            await interaction.followup.send("選個比賽好咪", view=game,ephemeral=True)
        else:
            await interaction.followup.send("沒比賽捏（其實是壞了)",ephemeral=True)
        
    @tasks.loop(seconds=10)
    async def statusloop(self,guild)-> None:
        # await asyncio.sleep(10)
        # try:
        #   user_amount=f"{len([m for m in self.bot.get_all_members() if not m.bot])} 位成員！嗨囉><"
        #   await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=user_amount))
        # except Exception as e:
        #     print(e)
      # await asyncio.sleep(10)
      print('execute')
      

    @statusloop.before_loop
    async def before_statusloop(self):
        await self.bot.wait_until_ready()
        print('Loop prepare...')

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
        return  # Ignore messages from bots

      content = str(message.content)
      
      # check if is twitter link
      if 'https://x.com/' in content:
        mention = message.author.mention
        c = content.replace('x.com','fxtwitter.com')
        response = f"{mention} : {c}"
        # emoji = '<:2CatMeeting:918811455325863966>'
        await message.delete()
        await message.channel.send(response)
      elif 'https://twitter.com/' in content:
        mention = message.author.mention
        c = content.replace('twitter.com','fxtwitter.com')
        response = f"{mention} : {c}"
        # emoji = '<:2CatMeeting:918811455325863966>'
        await message.delete()
        await message.channel.send(response)
      # elif '.com' in content:
      #   url = re.search("(?P<url>https?://[^\s]+)", content).group("url")
      #   url = unquote(url)
      #   await message.channel.send(url)
      
      # check if is @@, send message
      if "@@" in content:
        ran_num1 = random.randint(1, 10)
        if ran_num1 == 1:
          emoji = '<:2CatGloomy:917998978904240178>'
          await message.add_reaction(emoji)
          await message.channel.send("已發送 喜多喜多：他媽的...真的是被看扁了...")
        elif ran_num1 ==2 :
          emoji = '<:2CatBra:986271659692539985>'
          await message.add_reaction(emoji)
          reply="⠄⠄⠄⠄⠄⠄⢠⣿⣋⣿⣿⣉⣿⣿⣯⣧⡰⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⣿⣿⣹⣿⣿⣏⣿⣿⡗⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠟⡛⣉⣭⣭⣭⠌⠛⡻⢿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⠄⣤⡌⣿⣷⣯⣭⣿⡆⣈⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⣷⢛⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⠄⢻⣷⣽⣿⣿⣿⢿⠃⣼⣧⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣛⣻⣿⠟⣀⡜⣻⢿⣿⣿⣶⣤⡀⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⠄⢠⣤⣀⣨⣥⣾⢟⣧⣿⠸⣿⣿⣿⣿⣿⣤⡀⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⠄⢟⣫⣯⡻⣋⣵⣟⡼⣛⠴⣫⣭⣽⣿⣷⣭⡻⣦⡀⠄\n⠄⠄⠄⠄⠄⠄⠄⢰⣿⣿⣿⢏⣽⣿⢋⣾⡟⢺⣿⣿⣿⣿⣿⣿⣷⢹⣷⠄\n⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⢣⣿⣿⣿⢸⣿⡇⣾⣿⠏⠉⣿⣿⣿⡇⣿⣿⡆\n⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⢸⣿⣿⣿⠸⣿⡇⣿⣿⡆⣼⣿⣿⣿⡇⣿⣿⡇\n⠇⢀⠄⠄⠄⠄⠄⠘⣿⣿⡘⣿⣿⣷⢀⣿⣷⣿⣿⡿⠿⢿⣿⣿⡇⣩⣿⡇\n⣿⣿⠃⠄⠄⠄⠄⠄⠄⢻⣷⠙⠛⠋⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⡇⣿⣿⡇"
            
          await message.channel.send(reply)
  
        
        else:
            print("@@="+str(ran_num1))
      
      # check if is sticker, send hidden message
      if message.stickers:
        ran_num =random.randint(1,100)
        if ran_num==1:
          try:           
            reply ="||⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣷⣤⡀\n⠀⠀⠀⠀⠀⠀⢀⣾⡿⠋⠀⠿⠇⠉⠻⣿⣄\n⠀⠀⠀⠀⠀⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠙⣿⣆\n⠀⠀⠀⠀⢠⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣆\n⠀⠀⠀⠀⢸⣿⡄⠀⠀⠀⢀⣤⣀⠀⠀⠀⠀⣿⡿\n⠀⠀⠀⠀⠀⠻⣿⣶⣶⣾⡿⠟⢿⣷⣶⣶⣿⡟⠁\n⠀⠀⠀⠀⠀⠀⣿⡏⠉⠁⠀⠀⠀⠀⠉⠉⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⣸⣿⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⠀⠀⠀⣿⡇⢀⣴⣿⠇⠀⠀⠀⠀⣿⡇\n⠀⠀⠀⢀⣠⣴⣿⣷⣿⠟⠁⠀⠀⠀⠀⠀⣿⣧⣄⡀\n⠀⢀⣴⡿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⢿⣷⣄\n⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣆\n⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿\n⣿⣇⠀⠀⠀⠀⠀⠀⢸⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿\n⢹⣿⡄⠀⠀⠀⠀⠀⠀⢿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿\n⠀⠻⣿⣦⣀⠀⠀⠀⠀⠈⣿⣷⣄⡀⠀⠀⠀⠀⣀⣤⣾⡟⠁\n⠀⠀⠈⠛⠿⣿⣷⣶⣾⡿⠿⠛⠻⢿⣿⣶⣾⣿⠿⠛⠉⠀⠀||"
            await message.channel.send(reply)

          except Exception as e:
            print(f"Error in input_response: {e}")
        else:
          print("sticker="+str(ran_num))
      
      # check if is photo, store in db
      for attachment in message.attachments:
          if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
              print(f"Attachment in message from {message.author.name}")
              image_link = attachment.url
              guild_name = message.guild.name.replace(" ", "_")
              print(message.jump_url,image_link)
              store_pics(guild_name,message.author.name,message.channel.name,message.jump_url,image_link)
              emoji = '📸'  # Replace with your desired emoji
              await message.add_reaction(emoji)
      await self.bot.process_commands(message)

        

        

async def setup(bot: DBot) -> None:
    await bot.add_cog(util(bot))
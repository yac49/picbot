from typing import List
import discord
import sqlite3
import os

def dbcon():

    dbfolder = os.path.join(os.path.dirname(__file__), '../db')

    # Ensure the folder exists, you can skip this if you are certain it exists
    if not os.path.exists(dbfolder):
        os.makedirs(dbfolder)

    # Specify the full or relative path to the SQLite database file
    database_file = os.path.join(dbfolder, 'pic_data.db')

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    return conn, cursor

def store_pics(guild_name,name, channel, jump, img):
    # Connect to the SQLite database
    conn, cursor = dbcon()

    # Create a table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {guild_name}_pics (
            name TEXT,
            channel TEXT,
            jump TEXT,
            img TEXT UNIQUE
        )
    ''')

    # Insert the data into the table
    cursor.execute(f'''
        INSERT OR IGNORE INTO {guild_name}_pics (name, channel, jump, img)
        VALUES (?, ?, ?, ?)
    ''', (name, channel, jump, img))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(name, channel, jump, img)



def get_pics(guild_name,channel):
    # Connect to the SQLite database
    conn, cursor = dbcon()

    # Retrieve all the rows from the table
    cursor.execute(f'''SELECT * FROM {guild_name}_pics WHERE channel=?''',(channel,))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()
    if len(rows)>0:
      # rows.reverse()
    # Convert rows into embeds
      embeds = []
      for row in rows:
          name, channel, jump, img = row
          embed = discord.Embed(title=f"from {name} in {channel}", description=jump)
          embed.set_thumbnail(url=img)
          embeds.append(embed)

      embeds.reverse()
      return embeds
    else:
      return


class PicView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction,embedlist:List[discord.Embed], page_size=5):
        super().__init__(timeout=20)
        self.interaction = interaction
        self.embedlist = embedlist
        self.page_size = page_size
        self.current_page = 0
        self.message_sent = False
        # self.message = None


    async def show_embed(self):
      # Calculate the start and end index of the embeds to be shown
      start_index = self.current_page * self.page_size
      end_index = min(start_index + self.page_size, len(self.embedlist))
  
      # Get the embeds for the current page
      embeds = self.embedlist[start_index:end_index]
  
      # Send all embeds in one message
      try:
          if not self.message_sent:  # Change this line
              await self.interaction.response.send_message(embeds=embeds, view=self,ephemeral=True)
              self.message_sent = True  # Add this line
          else:
              await self.interaction.edit_original_response(embeds=embeds, view=self)
      except Exception as e:
          print(e)

    async def on_timeout(self):
        await self.interaction.edit_original_response(content="時間到嚕",embed=None,view=None)

    @discord.ui.button(label='上一頁', style=discord.ButtonStyle.primary)
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
         
          if self.current_page > 0:
              self.current_page -= 1
              await self.show_embed()
        except:
          pass


    @discord.ui.button(label='下一頁', style=discord.ButtonStyle.primary)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
          
          total_pages = len(self.embedlist) // self.page_size
          if self.current_page < total_pages:
              self.current_page += 1
              await self.show_embed()
        except:
          pass


import os
import discord
import requests
from datetime import datetime,timedelta
import os

from table2ascii import table2ascii
import json

game_key =os.getenv('GAME_KEY')

def get_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def get_yesterday(day):
    yesterday = day - timedelta(days=1)
    return yesterday

def get_nba_games(date):
    url = "https://v2.nba.api-sports.io/games?date="+str(date)
    payload={}
    headers = {
    'x-rapidapi-key': game_key,
    'x-rapidapi-host': 'v2.nba.api-sports.io'
    }
    re = requests.request("GET", url, headers=headers, data=payload)
    fetch= re.json()
    print("call once at"+str(datetime.today())+"\n")
    games = fetch['results']
    if games == 0:
        return get_nba_games(get_yesterday(date))
    else:
        print(games)
        return games,fetch
    
def get_nba():
    today = datetime.today()
    print(today)
    date_only = today.date()

    tables={}
    game_titles={}
    print(date_only)
    game, fetched = get_nba_games(date_only)

    for i in range(0,game):
        game_data = fetched['response'][i]
        game_title,table =create_table(game_data)
        game_titles[game_title[0]]=game_title
        tables[game_title[0]]=table
    return game_titles,tables

def ifPistonWin():
  today = datetime.today()
  print(today)
  date_only = today.date()

  print(date_only)
  game, fetched = get_nba_games(date_only)
  for i in range(0,game):
      game_data = fetched['response'][i]

      game_title = game_data['teams']['visitors']['name']+" vs "+game_data['teams']['home']['name']
      visitor_name=game_data['teams']['visitors']['name']
      home_name=game_data['teams']['home']['name']
      status_string=game_data['status']['long']
      if status_string=="Finished" and "Pistons" in visitor_name:
          pistons_total=game_data['scores']['visitors']['points']
          op_total =game_data['scores']['home']['points']
          break
      elif status_string=="Finished" and "Pistons" in home_name:
          pistons_total=game_data['scores']['home']['points']
          op_total =game_data['scores']['visitors']['points']
          break
  if pistons_total<op_total:
      return game_title,0
  elif pistons_total>op_total:
      return game_title,1

def create_table(game_data):
    game_title = (game_data['id'],game_data['teams']['visitors']['name']+" vs "+game_data['teams']['home']['name'])

    status_string=game_data['status']['long']
    if status_string != "Finished":
        if game_data['status']['clock']:
            status_string = str(game_data['status']['clock'])
        else:
            status_string = "EO" + str(game_data['periods']['current'])
    else:
        status_string = "Fin"

    visitor_name = game_data['teams']['visitors']['code']
    home_name = game_data['teams']['home']['code']

    column_labels = [status_string, '1', '2', '3', '4', 'Final']

    if len(game_data['scores']['home']['linescore']) == 5 or len(game_data['scores']['visitors']['linescore']) == 5:
        column_labels.insert(5, 'OT')
        column_labels.remove(status_string)
        table_data = [
            [game_data['scores']['visitors']['linescore'][i] for i in range(len(game_data['scores']['visitors']['linescore']))] + [game_data['scores']['visitors']['points']],
            [game_data['scores']['home']['linescore'][i] for i in range(len(game_data['scores']['home']['linescore']))] + [game_data['scores']['home']['points']],    
        ]
    else:
        table_data = [
            [visitor_name] + [game_data['scores']['visitors']['linescore'][i] for i in range(len(game_data['scores']['visitors']['linescore']))] + [game_data['scores']['visitors']['points']],
            [home_name] + [game_data['scores']['home']['linescore'][i] for i in range(len(game_data['scores']['home']['linescore']))] + [game_data['scores']['home']['points']],    
        ]
    table = table2ascii(header=column_labels,body=table_data)
    print(game_title)
    print(status_string)
    # print(table)
    return game_title,table

class NBAView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction,timeout=20):
        try:
            super().__init__(timeout=timeout)
            self.interaction = interaction
            game_titles, tables = get_nba()
            self.add_item(SelectGame(game_titles, tables))
        except Exception as e:
            print(e)
    async def on_timeout(self):

        re = await self.interaction.original_response()
        await re.edit(content="時間到嚕",view=None)
def getOptions(game_titles):
    try:
        info = list(game_titles.values())
        options = [
            discord.SelectOption(label=info[i][1], value=info[i][0]) for i in range(0,len(info))
        ]
        return options
    except Exception as e:
        print(e)

class SelectGame(discord.ui.Select):
    def __init__(self,game_titles,tables):
        try:
            self.game_titles=game_titles
            self.tables=tables
            super().__init__(placeholder="Select a game", options=getOptions(game_titles))
            print("SelectGame")
        except Exception as e:
            print(e)

    async def callback(self, interaction: discord.Interaction):
        try:
            title = self.game_titles[int(interaction.data['values'][0])][1]
            game_id = int(interaction.data['values'][0])
            message = self.tables[game_id]
            
            await interaction.response.edit_message(content=title+"```"+message+"```", view=self.view)
        except Exception as e:
            print(f'Error in interaction: {e}')

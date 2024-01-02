from bs4 import BeautifulSoup
import requests
import discord

def get_joke():
    api_url = 'https://readme-jokes.vercel.app/api'
    response = requests.get(api_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    question_element = soup.find('p', class_='question')
    answer_element = soup.find('p', class_='answer')

    if question_element and answer_element:
        question = question_element.get_text(strip=True)
        answer = answer_element.get_text(strip=True)
        return {'question': question, 'answer': answer}
    else:
        return {'error': 'I\'m a programmed bot, not a comedian.'}


def dad():
    jk=get_joke()
    if 'error' in jk:
        embed = discord.Embed(description=str(jk['error']), color=0xafc1d6)
    else:
        embed = discord.Embed(title=str(jk['question']), description="=> ||"+str(jk['answer'])+"||", color=0xafc1d6)
    return embed

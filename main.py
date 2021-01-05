import discord
import os
import keep_alive
import requests as reqs

client = discord.Client()

def get_quote():
  response = reqs.get('https://insult.mattbas.org/api/insult')
  quote = "@MEE6 " + response.text
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('GG') and message.author.bot:
    quote = get_quote()
    await message.channel.send(quote)

keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))

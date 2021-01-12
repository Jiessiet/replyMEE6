import discord
import os
import keep_alive
import requests
import json
import random
from replit import db
from discord.ext import commands

api_key = "your_api_key"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

bot = commands.Bot(command_prefix='!')
client = discord.Client()


def get_quote():
  response = requests.get('https://insult.mattbas.org/api/insult')
  quote = "@MEE6 " + response.text
  return(quote)

def get_weather():
  weather.weather()

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
  if message.content.startswith('!'):
    quote = weather()

@bot.command()
async def weather(ctx, *, city: str):
  city_name = city
  complete_url = base_url + "appid=" + api_key + "&q=" + city_name
  response = requests.get(complete_url)
  x = response.json()
  channel = ctx.message.channel
  if x["cod"] != "404":
      async with channel.typing():
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_celsiuis = str(round(current_temperature - 273.15))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        weather_description = z[0]["description"]
        embed = discord.Embed(title=f"Weather in {city_name}",
                          color=ctx.guild.me.top_role.color,
                          timestamp=ctx.message.created_at,)
        embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
        embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
        embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
        embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await channel.send(embed=embed)
  else:
        await channel.send("City not found.")

keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))

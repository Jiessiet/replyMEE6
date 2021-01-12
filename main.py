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

@client.event
async def remind(self, message, stripped, server):

        args = stripped.split(' ')

        if len(args) < 2:
            await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['no_argument'].format(prefix=server.prefix)))
            return

        scope = message.channel.id
        pref = '#'

        if args[0].startswith('<'): # if a scope is provided

            scope, pref = self.parse_mention(message, args[0], server)
            if scope is None:
                await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_tag']))
                return

            args.pop(0)

        try:
            while args[0] == '':
                args.pop(0)

            msg_time = self.format_time(args[0], server)
        except ValueError:
            await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_time']))
            return

        if msg_time is None:
            await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_time']))
            return

        args.pop(0)

        msg_text = ' '.join(args)

        if self.count_reminders(scope) > 5 and not self.get_patrons(message.author.id):
            await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_count'].format(prefix=server.prefix)))
            return

        if self.length_check(message, msg_text) is not True:
            if self.length_check(message, msg_text) == '150':
                await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_chars'].format(len(msg_text), prefix=server.prefix)))

            elif self.length_check(message, msg_text) == '2000':
                await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['invalid_chars_2000']))

            return

        if pref == '#':
            if not self.perm_check(message, server):
                await message.channel.send(embed=discord.Embed(description=self.get_strings(server)['remind']['no_perms'].format(prefix=server.prefix)))
                return

        print('Registered a new reminder for {}'.format(message.guild.name))

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

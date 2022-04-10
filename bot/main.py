import discord
import requests
import os
from replit import db
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Getting the data of cryptocurrencies

def getCrypocurrencyPrices(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  userRequest = requests.get(url=URL)
  data = userRequest.json()

  # Storing crypto data such as prices into the replit db
  for i in range(len(data)): #loop through the crypto data
    db[data[i]['id']] = data[0]['current_price'] # Storing the value to be bitcoin's current price
  if crypto in db.keys():
    return db[crypto]
  else:
    return None

# This function checks if a cryptocurrency is supported by this bot

def isCryptoSupported(crypto):
  if crypto in db.keys():
    return True
  else:
    return False

getCrypocurrencyPrices('bitcoin')

# Creating an instance of the discord client
client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  channel = discord.utils.get(client.get_all_channels(), name='general')

  await client.get_channel(channel.id).send('The Crypto Bot is now Online!')

# This is called whenever there is a message put into the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('Bitcoin'):
    await message.channel.send('This bot will fetch the price!')

client.run(BOT_TOKEN)
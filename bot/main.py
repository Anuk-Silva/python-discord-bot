import discord
import requests
from replit import db
from threading import Timer

# Check whether or not the price targets input by the user are valid integers
def check(priceTargets):
  try:
    return all(isinstance(int(x),int) for x in priceTargets)
  except:
    return False

# Getting the data of cryptocurrencies

def getCrypocurrencyPrices(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  userRequest = requests.get(url=URL)
  data = userRequest.json()

  # Storing crypto data such as prices into the replit db
  for i in range(len(data)): #loop through the crypto data
    db[data[i]['id']] = data[i]['current_price'] # Storing the value to be bitcoin's current price
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

def checkPriceTrend(startPrice,endPrice,priceTargets):
    if startPrice < endPrice:
        return normal_alert(startPrice,endPrice)
    elif startPrice == endPrice:
        return []
    else:
        return reverse_alert(startPrice,endPrice,priceTargets)
        
def reverse_alert(startPrice,endPrice,priceTargets):
    noti = []
    priceTargets = priceTargets[::-1]
    for priceTarget in priceTargets:
        if endPrice <= priceTarget:
            noti.append(priceTarget)
        else:
            continue
    return noti
 
def normal_alert(startPrice,endPrice,priceTargets):
    noti = []
    for priceTarget in priceTargets:
        if priceTarget <= endPrice:
            noti.append(priceTarget)
        else:
            continue
    return noti

def checkTwoListOrder(list1,list2):
    sorted_elements_1 = [list1[index] <= list1[index+1] for index in range(len(list1)-1)]
    sorted_elements_2 = [list2[index] <= list2[index+1] for index in range(len(list2)-1)]
    return all(sorted_elements_1) and all(sorted_elements_2)

# Send a discord notificaiton to a channel
async def sendMessageToDiscord(message):
  await discord.utils.get(client.get_all_channels(),name='general').send(message)

# Detecting for price alerts
async def detectPriceAlert(crypto, priceTargets):
  current_price = getCrypocurrencyPrices(crypto)

  if db['hitPriceTarget'] not in range(min(current_price,db['hitPriceTarget']),max(current_price,db['hitPriceTarget'])+1) and min(priceTargets) <= current_price <= max(priceTargets):
        db['hitPriceTarget'] = 0
  else:
    # compute noti
    if len(checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets)) != 0:
        if db['noti']!= checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets):
            # increasing in value: 
            if db['hitPriceTarget'] < current_price:
                if checkTwoListOrder(normal_alert(db['hitPriceTarget'],current_price),db['noti']):
                  for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price)) - set(db["noti"])):
                      await sendMessageToDiscord(f'The price of {crypto} has just passed {priceTarget} USD. The current price is: {current_price} USD.')
                else:
                  for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price)) - set(db["noti"])):
                    await sendMessageToDiscord(f'The price of {crypto} has just passed {priceTarget} USD. The current price is: {current_price} USD.')
                
            # decreasing in value:
            elif db['hitPriceTarget'] >= current_price:
                if checkTwoListOrder(reverse_alert(db['hitPriceTarget'],current_price,priceTargets),db["noti"]):
                  for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                    await sendMessageToDiscord(f'The price of {crypto} has just fallen below {priceTarget} USD. The current price is: {current_price} USD.')
                else:
                  for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                    await sendMessageToDiscord(f'The price of {crypto} has just fallen below {priceTarget} USD. The current price is: {current_price} USD.')
            else:
                pass

        if db['hitPriceTarget'] < current_price:
            db["noti"]= normal_alert(db['hitPriceTarget'],current_price)
            db['hitPriceTarget'] = max(normal_alert(db['hitPriceTarget'],current_price))
            
        if db['hitPriceTarget'] > current_price:
            db["noti"]= reverse_alert(db['hitPriceTarget'],current_price,priceTargets)
            db['hitPriceTarget'] = min(reverse_alert(db['hitPriceTarget'],current_price,priceTargets))
            
    else:
        db['hitPriceTarget'] = 0

  # Set a thread which runs and executes the detectPriceAlert function every 5 seconds
  Timer(5.0, await detectPriceAlert(crypto, priceTargets)).start()
  print("Finished")



# Creating an instance of the discord client
client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  channel = discord.utils.get(client.get_all_channels(), name='general')

  db['hitPriceTarget'] = 0
  db['noti'] = []

  await client.get_channel(channel.id).send('The Crypto Bot is now Online!')

# This is called whenever there is a message put into the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('ya'):
    await message.channel.send('yeet')
    
  # Send the crypto price directly
  if message.content.lower() in db.keys():
    await message.channel.send(f'The current price of {message.content} is: ${getCrypocurrencyPrices(message.content.lower())} USD')

  # List all the available cryptocurrencies
  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  # Check whether or not a cryptocurrency is supported by the bot
  if message.content.startswith('$support '):
    cryptocurrencyToBeChecked = message.content.split('$support', 1)[1].lower()
    await message.channel.send(isCryptoSupported(cryptocurrencyToBeChecked))

  # Setting multiple price alerts
  if message.content.startswith('$set '):
    messageList = message.content.split(' ')
    concernedCrypto = messageList[1]

    priceTargets = []
    for i in range(len(messageList) - 2):
      priceTargets.append(int(messageList[2 + i]))

    # Input validation for doubles and floats
    if isCryptoSupported(concernedCrypto) and check(priceTargets):
      db['detect crypto'] = concernedCrypto
      db['detect price'] = priceTargets

      await message.channel.send(f'Successfully set price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')

    else:
      await message.channel.send(f'Unsuccessful setting of the price alerts which you have specified. Please Try Again!.')

  if message.content.startswith('$start'):
    await message.channel.send(f'Started detecting price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')
    await detectPriceAlert(db["detect crypto"], db["detect price"])

client.run(BOT_TOKEN)
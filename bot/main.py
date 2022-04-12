import discord
import requests
from replit import db
from threading import Timer
from keep_running import keep_running

# Check whether or not the price targets input by the user are valid integers
def check(goalsForPrice):
  try:
    return all(isinstance(int(x),int) for x in goalsForPrice)
  except:
    return False

# Getting the data of cryptocurrencies
def getPricesOfCryptocurrency(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  usdR = requests.get(url=URL)
  dataUSD = usdR.json()

  for i in range(len(dataUSD)): # Loop through the crypto dataNZD
    db[dataUSD[i]['id']] = dataUSD[i]['current_price'] # Storing the value to be bitcoin's current price

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

def getPricesOfCryptocurrencyNZD(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=nzd'
  nzdR = requests.get(url=URL)
  dataNZD = nzdR.json()

 # Storing crypto dataNZD such as prices into the replit db
  for i in range(len(dataNZD)): # Loop through the crypto dataNZD
    db[dataNZD[i]['id']] = dataNZD[i]['current_price'] # Storing the value to be bitcoin's current price in NZD

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

def getMarketCapOfCryptocurrencyNZD(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=nzd'
  nzdMCR = requests.get(url=URL)
  dataMCNZD = nzdMCR.json()

 # Storing crypto dataNZD such as market cap into the replit db
  for i in range(len(dataMCNZD)): # Loop through the crypto dataNZD
    db[dataMCNZD[i]['id']] = dataMCNZD[i]['market_cap'] # Storing the value to be bitcoin's current market cap value

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

# This function checks if a cryptocurrency is supported by this bot
def isThisCryptoTracked(crypto):
  if crypto in db.keys():
    return "This cryptocurrency is supported by the Crypto Price-Info Bot!"
  else:
    return "Unfortunately, this cryptocurrency is not supported by the Crypto Price-Info Bot at the moment!"

def checkPriceActivity(startPrice,endPrice,priceTargets):
    if startPrice < endPrice:
        return normal_alert(startPrice,endPrice,priceTargets)
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

# Send a discord notification to a channel
async def sendMessage(message):
  await discord.utils.get(client.get_all_channels(),name='general').send(message)

# Detecting for price alerts
async def detectPriceAlert(crypto,priceTargets):
  current_price = getPricesOfCryptocurrency(crypto)

  if db['hitPriceTarget'] not in range(min(current_price,db['hitPriceTarget']),max(current_price,db['hitPriceTarget'])+ 1.00 and min(priceTargets) <= current_price <= max(priceTargets)):
        db['hitPriceTarget'] = 0
  else:
      # compute noti
      if len(checkPriceActivity(db['hitPriceTarget'],current_price,priceTargets)) != 0:
          if db['noti']!= checkPriceActivity(db['hitPriceTarget'],current_price,priceTargets):
              # When the value is increasing: 
              if db['hitPriceTarget'] < current_price:
                  if checkTwoListOrder(normal_alert(db['hitPriceTarget'],current_price, priceTargets),db['noti']):
                    for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price, priceTargets)) - set(db["noti"])):
                        await sendMessage(f'The price of {crypto} has just passed ${priceTarget} USD. The current price is: {current_price} USD.')
                  else:
                    for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price, priceTargets)) - set(db["noti"])):
                      await sendMessage(f'The price of {crypto} has just passed ${priceTarget} USD. The current price is: {current_price} USD.')
                  
              # When the value is decreasing: 
              elif db['hitPriceTarget'] >= current_price:
                  if checkTwoListOrder(reverse_alert(db['hitPriceTarget'],current_price,priceTargets),db["noti"]):
                    for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                      await sendMessage(f'The price of {crypto} has just fallen below ${priceTarget} USD. The current price is: {current_price} USD.')
                  else:
                    for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                      await sendMessage(f'The price of {crypto} has just fallen below ${priceTarget} USD. The current price is: {current_price} USD.')
              else:
                  pass
  
          if db['hitPriceTarget'] < current_price:
              db["noti"]= normal_alert(db['hitPriceTarget'],current_price, priceTargets)
              db['hitPriceTarget'] = max(normal_alert(db['hitPriceTarget'],current_price, priceTargets))
              
          if db['hitPriceTarget'] > current_price:
              db["noti"]= reverse_alert(db['hitPriceTarget'],current_price,priceTargets)
              db['hitPriceTarget'] = min(reverse_alert(db['hitPriceTarget'],current_price,priceTargets))
              
      else:
          db['hitPriceTarget'] = 0

  # Set a thread which runs and executes the detectPriceAlert function every 5 seconds
  Timer(5.0, await detectPriceAlert(crypto,priceTargets)).start() 
  print("--Finished--")



# Creating an instance of the discord client
client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Crypto Market!"))
  channel = discord.utils.get(client.get_all_channels(),name='general')

  db['hitPriceTarget'] = 0
  db['noti'] = []

  await client.get_channel(channel.id).send('The Crypto Price-Info Bot is now online!')

# This is called whenever there is a message put into the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  prefix = "!"
  if (message.content[0] == prefix):
    command = message.content.split(" ")[0]

    print(command)
  
    if(command == prefix + "price"):
      cryptoToBePriced = message.content.split('!price ',1)[1].lower()
      print(cryptoToBePriced)
      if (cryptoToBePriced.lower() in db.keys()):
        await message.channel.send(f'The current price of {cryptoToBePriced} is: ${getPricesOfCryptocurrency(cryptoToBePriced.lower())} USD')

    if(command == prefix + "pricenz"):
      cryptoToBePriced = message.content.split('!pricenz ',1)[1].lower()
      print(cryptoToBePriced)
      if (cryptoToBePriced.lower() in db.keys()):
        await message.channel.send(f'The current price of {cryptoToBePriced} is: ${getPricesOfCryptocurrencyNZD(cryptoToBePriced.lower())} NZD')

    if(command == prefix + "mcnz"):
      marketCapToBeChecked = message.content.split('!mcnz ',1)[1].lower()
      print(marketCapToBeChecked)
      if (marketCapToBeChecked.lower() in db.keys()):
        await message.channel.send(f'The current value of {marketCapToBeChecked}s Market Cap is: ${getMarketCapOfCryptocurrencyNZD(marketCapToBeChecked.lower())} NZD')

  # Send the crypto price directly
  #if message.content.lower() in db.keys():
  #  await message.channel.send(f'The current price of {message.content} is:   ${getPricesOfCryptocurrency(message.content.lower())} USD')

  # List all the available cryptocurrencies
  if message.content.startswith('!list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  # Check whether or not a cryptocurrency is supported by the bot
  if message.content.startswith('!support '):
    cryptoToBeChecked = message.content.split('!support ',1)[1].lower()
    await message.channel.send(isThisCryptoTracked(cryptoToBeChecked))

  # Setting multiple price alerts
  if message.content.startswith('!set '):
    messageList = message.content.split(' ')
    cryptoConcerned = messageList[1]

    priceTargets = []
    for i in range(len(messageList) - 2):
      priceTargets.append(int(messageList[2 + i]))

    # Input validation for doubles and floats
    if isThisCryptoTracked(cryptoConcerned) and check(priceTargets):
      db['detect crypto'] = cryptoConcerned
      db['detect price'] = priceTargets

      await message.channel.send(f'Successfully set price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')

    else:
      await message.channel.send(f'Unsuccessful setting of price alerts. Please try again.')

  if message.content.startswith('!start'):
    await message.channel.send(f'Started detecting price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')
    await detectPriceAlert(db["detect crypto"],db["detect price"])


keep_running()

client.run(BOT_TOKEN)
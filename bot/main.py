import discord
from replit import db
from threading import Timer
from keep_running import keep_running
from discord.ext import commands
from functions import check, getPricesOfCryptocurrencyUSD, getPricesOfCryptocurrencyNZD, getMarketCapOfCryptocurrencyNZD, getImageOfCryptocurrency, isThisCryptoTracked, checkPriceActivity, reverse_alert, normal_alert, checkTwoListOrder, get24HRChangeOfCryptocurrency, getMarketCapOfCryptocurrencyUSD, get24HRChangeofCryptocurrencyHighNZD, get24HRChangeofCryptocurrencyLowNZD


# Send a discord notification to a channel
async def sendMessage(message):
  await discord.utils.get(client.get_all_channels(),name='general').send(message)

# Detecting for price alerts
async def detectPriceAlert(crypto,priceTargets):
  current_price = getPricesOfCryptocurrencyUSD(crypto)

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
  for server in client.guilds:# guild stands for server
    requiredChannel = discord.utils.get(server.channels, name = 'cryptobot')
    await requiredChannel.send("The Crypto Price-Info Bot is now online!")

  db['hitPriceTarget'] = 0
  db['noti'] = []
                
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
        await message.channel.send(f'The current price of {cryptoToBePriced} is: ${getPricesOfCryptocurrencyUSD(cryptoToBePriced.lower())} USD')

    if(command == prefix + "pricenz"):
      cryptoToBePriced = message.content.split('!pricenz ',1)[1].lower()
      print(cryptoToBePriced)
      if (cryptoToBePriced.lower() in db.keys()):
        await message.channel.send(f'The current price of {cryptoToBePriced} is: ${getPricesOfCryptocurrencyNZD(cryptoToBePriced.lower())} NZD')

    if(command == prefix + "mc"):
      marketCapToBeChecked = message.content.split('!mc ',1)[1].lower()
      print(marketCapToBeChecked)
      if (marketCapToBeChecked.lower() in db.keys()):
        await message.channel.send(f'The current value of {marketCapToBeChecked}s Market Cap is: ${getMarketCapOfCryptocurrencyUSD(marketCapToBeChecked.lower())} USD')
        
    if(command == prefix + "mcnz"):
      marketCapToBeChecked = message.content.split('!mcnz ',1)[1].lower()
      print(marketCapToBeChecked)
      if (marketCapToBeChecked.lower() in db.keys()):
        await message.channel.send(f'The current value of {marketCapToBeChecked}s Market Cap is: ${getMarketCapOfCryptocurrencyNZD(marketCapToBeChecked.lower())} NZD')

    if(command == prefix + "image"):
      imageToBeRetrieved = message.content.split('!image ',1)[1].lower()
      print(imageToBeRetrieved)
      if (imageToBeRetrieved.lower() in db.keys()):
        await message.channel.send(getImageOfCryptocurrency(imageToBeRetrieved.lower()))
        
    if(command == prefix + "creator"):
      embed=discord.Embed(
      title="About the developer",
      url="https://github.com/Anuk-Silva", 
      description= "Hi there, My name is Anuk. I built this bot on python and this bot basically tracks and monitors the prices of various cryptocurrencies. Use !help to view a list of commands you may use :)",
    )
      embed.set_image(url ='https://assets.coingecko.com/coins/images/6799/large/BSV.png?1558947902%27,')
      embed.set_thumbnail(url='https://avatars.githubusercontent.com/u/83688599?v=4')

      await message.channel.send(embed=embed)

    if(command == prefix + "24hrnzd"):
      coinDailyDataToGet = message.content.split('!24hr ',1)[1].lower()
      if (coinDailyDataToGet.lower() in db.keys()):
        print(coinDailyDataToGet)
        priceChangePercentage = str(get24HRChangeOfCryptocurrency(coinDailyDataToGet.lower()))
        print(priceChangePercentage)
        priceChangeHighNZD = str(get24HRChangeofCryptocurrencyHighNZD(coinDailyDataToGet.lower()))
        print(priceChangeHighNZD)
        await message.channel.send(f'{coinDailyDataToGet.capitalize()} had a {get24HRChangeOfCryptocurrency(coinDailyDataToGet.lower())}% change in the last 24 hours')
        priceChangeLowNZD = str(get24HRChangeofCryptocurrencyLowNZD(coinDailyDataToGet.lower()))
        print(priceChangeLowNZD)
          

    if(command == prefix + "help"):
      embed=discord.Embed(
      color=0xe74c3c,
      title="Crypto Price-Info Bot Help Section",
      description= (f' Below are some useful commands to utilise this bot')
    )
      embed.add_field(name="!support <coin>", value="Checks if the coin is supported by the Bot", inline = False)
      embed.add_field(name="!list", value="Provides a list of coins which is supported and tracked by the Bot", inline = False)
      embed.add_field(name="!price <coin>", value="Fetch the current price of a coin in USD", inline = False)
      embed.add_field(name="!pricenz <coin>", value="Fetch the current price of a coin in NZD", inline = False)
      embed.add_field(name="!24hr <coin>", value="Fetch the change in price from the last 24 hours in a percentage format", inline = False)
      embed.add_field(name="!mcnz <coin>", value="Fetch the current value of the coin's Market Cap in NZD", inline = False)
      embed.add_field(name="!set <coin> [pricetargets]", value="Sets a range of price targets for a particular coin. The Bot will notify if a price target has been reached and/or drops below a price target. Use comma to separate each different price target", inline = False)
      embed.add_field(name="!start", value="The Bot will start monitoring the price activity of the coin and notify if any specified price target has been reached", inline = False)
      embed.add_field(name="!about", value="The Bot will display a list of information related to the coin such as price, market cap and more!", inline = False)
      embed.add_field(name="!help", value="The Bot will display a list of useful commands which you can use to fetch data of a coin and more!", inline = False)
      embed.set_image(url ='https://datafloq.com/wp-content/uploads/2021/12/blog_pictures2FCryptocurrency.jpeg'),
      embed.set_thumbnail(url = 'https://gmgfinancial.com/wp-content/uploads/2021/03/Crypto-Big.jpg')
      await message.channel.send(embed=embed)

    if(command == prefix + "about"):
      cryptoAboutToBeChecked = message.content.split('!about ',1)[1].lower()
      print(cryptoAboutToBeChecked)
      if (cryptoAboutToBeChecked.lower() in db.keys()):
        coinImage = getImageOfCryptocurrency(cryptoAboutToBeChecked)
        embed=discord.Embed(
          color=0xe74c3c,
          title="About " +cryptoAboutToBeChecked.capitalize(),
          description= (f'About {cryptoAboutToBeChecked.capitalize()} and other related data!')
        )
        embed.add_field(name="Current Price in USD", value=f'The current value of {cryptoAboutToBeChecked}s price is: ${getPricesOfCryptocurrencyUSD(cryptoAboutToBeChecked.lower())} USD', inline = False)
        embed.add_field(name="Current Price in NZD", value=f'The current value of {cryptoAboutToBeChecked}s price is: ${getPricesOfCryptocurrencyNZD(cryptoAboutToBeChecked.lower())} NZD', inline = False)
        embed.add_field(name=f'{cryptoAboutToBeChecked.capitalize()}s Market Cap value in USD is ', value=f'${getMarketCapOfCryptocurrencyUSD(cryptoAboutToBeChecked.lower())}', inline = False)
        embed.add_field(name=f'{cryptoAboutToBeChecked.capitalize()}s Market Cap value in NZD is ', value=f'${getMarketCapOfCryptocurrencyNZD(cryptoAboutToBeChecked.lower())}', inline = False)
        embed.add_field(name="Price Change in last 24 Hours", value=f'The price change of {cryptoAboutToBeChecked}s in the last 24 hours is: {str(get24HRChangeOfCryptocurrency(cryptoAboutToBeChecked.lower()))}%', inline = False)
        embed.set_image(url=coinImage)
        embed.set_thumbnail(url = 'https://gmgfinancial.com/wp-content/uploads/2021/03/Crypto-Big.jpg')
        await message.channel.send(embed=embed)

  # Send the crypto price directly
  #if message.content.lower() in db.keys():
  #  await message.channel.send(f'The current price of {message.content} is:   ${getPricesOfCryptocurrencyUSD(message.content.lower())} USD')

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
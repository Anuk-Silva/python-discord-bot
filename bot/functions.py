from replit import db
import requests

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

def getImageOfCryptocurrencyNZD(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=nzd'
  nzdImageR = requests.get(url=URL)
  dataImageNZD = nzdImageR.json()

 # Storing crypto dataNZD such as market cap into the replit db
  for i in range(len(dataImageNZD)): # Loop through the crypto dataNZD
    db[dataImageNZD[i]['id']] = dataImageNZD[i]['image'] # Storing the value to be bitcoin's current market cap value

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

def get24HRChangeOfCryptocurrency(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=nzd'
  dailyChange = requests.get(url=URL)
  dailyChangeData = dailyChange.json()

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
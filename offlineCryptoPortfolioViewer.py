#!/usr/bin/env python3

import requests
import json
import math
import time
import locale
import os
import sched, time
import sys
from termcolor import colored, cprint
from prettytable import PrettyTable

### USAGE ####
# Created by SnoothDogg 2018
# Browse to this URL: https://api.coinmarketcap.com/v2/ticker/ and find the token "id" + "name"
# Add/change them to coinId & totalToken as listed below, the below are just examples
# Then create a new variable above for your inital purchase price (e.g. day1_xx = 0.00)
# Then add that variable below to initalInvest (e.g. , day1_xx)
# Open portfolio.html in a browser and it will auto refresh with the results


## ***** Change to the number of tokens you purchased, below are examples  - ** MANDATORY **
""" NUMBER OF COINS/TOKENS GO HERE - Syntax: symbol = amount of coins """
btc = 1
eth = 1
xrp = 1


""" PURCHASE PRICE GOES HERE - Syntax: day1_symbol = purchase price"""
## ***** Change to how much you purchased them for, below are examples - ** MANDATORY **
day1_btc = 10
day1_eth = 0.0001
day1_xrp = 0.0001


""" FROM URL LISTED ABOVE APPEND THE BELOW THREE VARIABLES """
## Example Coins
# 1 - BTC (Bitcoin)
# 1027 - ETH (Ethereum)
# 52 - XRP (XRP)
# Change these variables, add/delete as needed - ** MANDATORY **
coinId = ['1','1027','52']
totalToken = [btc,eth,xrp]
initalIvest = [day1_btc,day1_eth,day1_xrp]

#### *************** DO NOT CHANGE BELOW ********************** ##
#### *************** DO NOT CHANGE BELOW ********************** ##

# Global Variables
refreshTimer = 5
maxCoins = coinId.__len__()
filename = "portfolio.txt"
maxToken = totalToken.__len__()

# Number Formatter
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Initialize the PrettyTable
prettyTable1 = PrettyTable(['Name', 'Token ID', 'Latest Prices', '% Change 1hr', '% Change 24hr', '% Change 7d', 'Total Token Value', 'Inital Investment', 'Margins'])

# REST GET JSON payload for selected COIN/TOKEN
def getTokenJson(index):
    url = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    return url

# GET AUD Prices - returns single price
def getAUDPrices(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    audPrices = results['data']['quotes']['AUD']['price']
    #print(json.dumps(results, sort_keys=True, indent=4))
    return audPrices

# Get TOKEN Name - returns single name
def getTokenName(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    #active = results['prices']['xrp']['ask'] # this is for coinspot
    audPrices = results['data']['name'] # this is for coinmarketcap
    #print(json.dumps(results, sort_keys=True, indent=4))
    return audPrices

# Get TOKEN Name - returns single name
def getTicker(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    #active = results['prices']['xrp']['ask'] # this is for coinspot
    y = results['data']['symbol'] # this is for coinmarketcap
    #print(json.dumps(results, sort_keys=True, indent=4))
    return y

# Get TOKEN Name - returns single name
def getP1H(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    #active = results['prices']['xrp']['ask'] # this is for coinspot
    y = results['data']['quotes']['AUD']['percent_change_1h'] # this is for coinmarketcap
    #print(json.dumps(results, sort_keys=True, indent=4))
    return y

def getP24H(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    #active = results['prices']['xrp']['ask'] # this is for coinspot
    y = results['data']['quotes']['AUD']['percent_change_24h'] # this is for coinmarketcap
    #print(json.dumps(results, sort_keys=True, indent=4))
    return y

def getP7D(index):
    x = 'https://api.coinmarketcap.com/v2/ticker/'+index+'/?convert=AUD'
    request = requests.get(x)
    results = request.json()
    #active = results['prices']['xrp']['ask'] # this is for coinspot
    y = results['data']['quotes']['AUD']['percent_change_7d'] # this is for coinmarketcap
    #print(json.dumps(results, sort_keys=True, indent=4))
    return y

def addDate():
    genTime = time.time()
    dateTime = time.ctime(int(genTime))
    prettyTable1.add_row([dateTime,"","","","","","","",""])

# Create a loop to add each entry to the prettyTable
def addToTable():
    addDate()
    i = 0
    while i < maxCoins:
        # retrieve data
        name = getTokenName(coinId[i])
        ticker = getTicker(coinId[i])
        latestPrices = getAUDPrices(coinId[i])
        percent1H = getP1H(coinId[i])
        percent24H = getP24H(coinId[i])
        percent7D = getP7D(coinId[i])
        totalTokenValue = '$'+locale.format_string('%.2f',(totalToken[i] * latestPrices),True)
        initalInvestment = '$'+locale.format_string('%.2f',(initalIvest[i] * totalToken[i]),True)
        totalMargin = '$'+locale.format_string('%.2f',(totalToken[i] * latestPrices) - (initalIvest[i] * totalToken[i]),True)

        prettyTable1.add_row([name, ticker, latestPrices, percent1H, percent24H, percent7D, totalTokenValue, initalInvestment, totalMargin])

        i = i + 1
    #prettyTable1.add_row(["","","","","","","","",""])
    #prettyTable1.add_row(["*****","*****","*****","*****","*****","*****","*****","*****","*****"])
    #prettyTable1.add_row(["","","","","","","","",""])

## Write to txt file
def writeToFile():
    file = open(filename, "w+")
    file.write(str(prettyTable1))
    file.write

## Remote txt file
def removeFile():
    os.remove(filename)

## Start a timer to refresh the prices and calculations every for whatever interval you set at the top
startTime = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    prettyTable1.clear_rows()
    addToTable()
    writeToFile()
    print(prettyTable1)
    startTime.enter(refreshTimer, 1, do_something, (sc,))

## Initialise()
startTime.enter(refreshTimer, 1, do_something, (startTime,))
startTime.run()

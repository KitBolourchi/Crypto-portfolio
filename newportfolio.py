from tkinter import *
import tkinter
from tkinter import font
import matplotlib.pyplot as plt
import json
from requests import Request, Session
import time
import pprint

from requests.api import get


def get_coin_id(crypto_sym):
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
  parameters = {
    'symbol' : crypto_sym,
    'aux':'status'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '36d40691-0746-41b3-872d-2fcc232d69c9',
  }

  session = Session()
  session.headers.update(headers)

  response = session.get(url, params=parameters)
  current_price = json.loads(response.text)['data']


  my_dict = {d['symbol']: d for d in current_price}
  return my_dict[crypto_sym]['id']


def get_price(crypto, id):
  url = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'slug': crypto,
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '36d40691-0746-41b3-872d-2fcc232d69c9',
  }

  session = Session()
  session.headers.update(headers)

  response = session.get(url, params=parameters)
  current_price = json.loads(response.text)['data'][f'{id}']['quote']['USD']['price']
  return current_price


def get_percent_change(crypto, id, time):
  url = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'slug': crypto,
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '36d40691-0746-41b3-872d-2fcc232d69c9',
  }

  session = Session()
  session.headers.update(headers)

  response = session.get(url, params=parameters)
  percent_change = json.loads(response.text)['data'][f'{id}']['quote']['USD'][time]
  return float(percent_change)


def profitOrLossColour(number):
  if number < 0:
    return 'red'
  elif number > 0:
    return 'green'
  else:
    return 'black'


def lookup():
  root.title('Crypto Currency Portfolio -- Last Updated: ' + time.strftime('%H:%M:%S'))

  portfolio = [
    {
      'symbol' : 'HBAR',
      'name' : 'hedera',
      'amount' : 878,
      'priceAtBuy' : 0.34
    },
    {
      'symbol' : 'AVAX',
      'name' : 'avalanche',
      'amount' : 10,
      'priceAtBuy' : 110
    },
    {
      'symbol' : 'HBAR',
      'name' : 'hedera',
      'amount' : 642,
      'priceAtBuy' : 0.324
    }
  ]

  portfolioInitialValue = 0
  portfolioCurrentValue = 0

  currencyCounter = 0
  pieNames = []
  pieSizes = []
  for c in portfolio:
    coin_id = get_coin_id(c['symbol'])
    currencyCounter += 1

    totalInvestedInCoin = c['amount'] * c['priceAtBuy']
    portfolioInitialValue += totalInvestedInCoin

    totalCoinCurrentWorth = c['amount'] * float(get_price(c['name'], coin_id))
    portfolioCurrentValue += totalCoinCurrentWorth

    totalROI = totalCoinCurrentWorth - totalInvestedInCoin
    percentualROI = ((totalCoinCurrentWorth / totalInvestedInCoin) * 100) - 100

    pieNames.append(c['name'])
    pieSizes.append(totalCoinCurrentWorth)

    time24 = get_percent_change(c['name'], coin_id, 'percent_change_24h')
    time7d = get_percent_change(c['name'], coin_id, 'percent_change_7d')
    
    symbol = Label(root, text=c['symbol'], font='Arial 12', bg='white')
    symbol.grid(row=currencyCounter, column=0, sticky=N + S + E + W)

    name = Label(root, text=c['name'], font='Arial 12', bg='silver')
    name.grid(row=currencyCounter, column=1, sticky=N + S + E + W)

    quantity = Label(root, text='{0:.6f}'.format(c['amount']), font='Arial 12', bg='white')
    quantity.grid(row=currencyCounter, column=2, sticky=N + S + E + W)

    initialPrice = Label(root, text='${0:.4f}'.format(c['priceAtBuy']), font='Arial 12', bg='silver')
    initialPrice.grid(row=currencyCounter, column=3, sticky=N + S + E + W)

    currentPrice = Label(root, text='${0:.4f}'.format(get_price(c['name'], coin_id)), font = 'Arial 12', bg='white')
    currentPrice.grid(row=currencyCounter, column=4, sticky= N + S + E + W)

    initialValue = Label(root, text='${0:.2f}'.format(totalInvestedInCoin), font='Arial 12', bg='silver')
    initialValue.grid(row=currencyCounter, column=5, sticky=N + S + E + W)

    currentValue = Label(root, text='${0:.2f}'.format(totalCoinCurrentWorth), font='Arial 12', bg='white')
    currentValue.grid(row=currencyCounter, column=6, sticky=N + S + E + W)

    percentualROI = Label(root, text='{0:.2f}%'.format(percentualROI), font='Arial 12', bg='silver', fg=profitOrLossColour(percentualROI))
    percentualROI.grid(row=currencyCounter, column=7, sticky=N + S + E + W)

    rOI = Label(root, text='${0:.2f}'.format(totalROI), font='Arial 12', bg='white', fg=profitOrLossColour(totalROI))
    rOI.grid(row=currencyCounter, column=8, sticky=N + S + E + W)

    change24hour = Label(root, text='{0:.2f}%'.format(time24), font='Arial 12', bg='silver', fg=profitOrLossColour(time24))
    change24hour.grid(row=currencyCounter, column=9, sticky=N + S + E + W)

    change7day = Label(root, text='{0:.2f}%'.format(time7d), font='Arial 12', bg='white', fg=profitOrLossColour(time7d))
    change7day.grid(row=currencyCounter, column=10, sticky=N + S + E + W)
  
  portfolioROI = portfolioCurrentValue - portfolioInitialValue
  portfolioPercentualROI = ((portfolioCurrentValue / portfolioInitialValue) * 100) - 100

  totalsLabel = Label(root, text='Totals', font='Arial 12 bold', bg='white')
  totalsLabel.grid(row=(currencyCounter + 1), column=0, sticky=N + S + E + W)

  portfolioInitialValueLabel = Label(root, text='${0:.2f}'.format(portfolioInitialValue), font='Arial 12', bg='silver')
  portfolioInitialValueLabel.grid(row=(currencyCounter + 1), column=5, sticky=N + S + E + W)

  portfolioCurrentValueLabel = Label(root, text='${0:.2f}'.format(portfolioCurrentValue), font='Arial 12', bg='white')
  portfolioCurrentValueLabel.grid(row=(currencyCounter + 1), column=6, sticky=N + S + E + W)

  portfolioPercentualROIlabel = Label(root, text='{0:.2f}%'.format(portfolioPercentualROI), font='Arial 12', bg='white', fg=profitOrLossColour(portfolioPercentualROI))
  portfolioPercentualROIlabel.grid(row=(currencyCounter + 1), column=7, sticky=N + S + E + W)

  portfolioROIlabel = Label(root, text='${0:.2f}'.format(portfolioROI), font='Arial 12', bg='silver', fg=profitOrLossColour(portfolioROI))
  portfolioROIlabel.grid(row=(currencyCounter + 1), column=8, sticky=N + S + E + W)

  update = Button(root, text='Update', command=lookup)
  update.grid(row=(currencyCounter + 1), column=10, sticky= N + E + S + W)

  def createPieGraph(labels, sizes):
    patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches, labels, loc='best')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

  pieChartButton = Button(root, text='Pie Chart', command= lambda: createPieGraph(pieNames, pieSizes))
  pieChartButton.grid(row=(currencyCounter + 1), column=9, sticky=N + S + E + W)


root = Tk()

headers = ['Symbol', 'Name', 'Quantity', 'Initial Price', 'Current Price', 'Initial Value', 'Current Value', '% ROI', 'ROI', '24 Hour Change', '7 Day Change']

headerCounter = 0
headerBGcolor = ''
for x in headers:
    if headerCounter % 2 == 1:
        headerBGcolor = 'silver'
    else:
        headerBGcolor = 'white'
    headerLabel = Label(root, text=x, font='Arial 15 bold', bg=headerBGcolor)
    headerLabel.grid(row=0, column=headerCounter, sticky=N + W + S + E)
    headerCounter += 1


lookup()

root.mainloop()









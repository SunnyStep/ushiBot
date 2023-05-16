import requests
import json
import time, os, asyncio
from database import sqlite_db
from colorama import Fore, Style
from handlers.botModules.roots import newTokenInfo
from handlers.controllers.states import *

try:
    web = os.getenv('BOTSIDE')
except:
    pass

async def getTokenList():
    url = "https://uanalytics-api.herokuapp.com/api/v1/token/top?page=0&size=10"
    headers = {
        "Host": "uanalytics-api.herokuapp.com",
        "Origin": "https://ushi.pro",
        "Referer": "https://ushi.pro/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru,en;q=0.9,uk;q=0.8,cy;q=0.7",
        "Connection": "close",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = json.loads(response.text)

        renewedList = []

        for item in json_data["content"][:10]:

            def refactorList():
                tokenData = {
                    "tokenLink": f'https://app.ushi.pro/token/{item["address"]}',
                    "tokenName": item['name'],
                    "symbol": item['symbol'],
                    "price": item['price'],
                    "dayDiff": item['price24hUsdDiff'],
                    "mcap": item['mcap'],
                    "liquidity": item['liquidityUsd'],
                    "dayVolume": item['volume24hUsd'],
                    "holders": item['holders'],
                }
                renewedList.append(tokenData)
                return renewedList
            refactorList()
        
        try:
            sqlite_db.sqlUpdateDay()    
            lastTokenList = sqlite_db.getLastTokenList()
        except:
            pass
        
        def compareLists(prevList, newList):
            newValues = {d['tokenLink'] for d in newList}
            missingValues = [value for value in newValues if value not in prevList]
            return missingValues
        
        difference = compareLists(lastTokenList, renewedList)
        
        if difference:
            
            def findTokenDataByLink(newList, alikeLink):
                for dictionary in newList:
                    if "tokenLink" in dictionary and dictionary["tokenLink"] == alikeLink:
                        return dictionary
            
            try:
                for alikeToke in difference:
                    tokenData = findTokenDataByLink(renewedList, alikeToke)
                    print(Fore.MAGENTA + '[NEW]' + Style.RESET_ALL, end=' ')
                    print(f'Обнаружен новый токен в Hot! – {tokenData["tokenName"]}')
                    await newTokenInfo(users=sqlite_db.sqlGetUserIds(), tokenData=tokenData)
                    
            except:
                pass
            
            
            
        sqlite_db.sqlAddTokenData(renewedList)  
        return renewedList   
    else:
        print("Ошибка запроса!")
    
async def checkCycle():
    while True:
        try:
            await getTokenList()
            time.sleep(400)
        except Exception as e:
            print("Критическая ошибка!", e)  # Добавьте отправку сообщения об ошибке
            break

async def startWeb(web):
    if web == 'web':
        sqlite_db.sql_start()
        await checkCycle()
        
asyncio.run(startWeb(web))
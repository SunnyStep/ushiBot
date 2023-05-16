import sqlite3 as sq
from colorama import Fore, Style 
import datetime

def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print(Fore.GREEN + '[OK]' + Style.RESET_ALL, end=' ')
        print('База данных успешно подключена.')
        
    base.commit()
    

def sqlUpdateDay():
    current_date = datetime.datetime.now()
    table_name = "day_" + current_date.strftime("%d%m%y")
    
    try:
        cur.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, tokenLink TEXT, tokenName TEXT, symbol TEXT, price TEXT, dayDiff INTEGER, mcap TEXT, liquidity TEXT, dayVolume TEXT, holders INTEGER)")
        print(f"Обновлена таблица нового дня: {table_name}")
    except Exception as e:
        pass
        
    base.commit()

def sqlAddTokenData(tokenList):
    current_date = datetime.datetime.now()
    table_name = "day_" + current_date.strftime("%d%m%y")
    
    try:
        sql = f'''
        INSERT INTO {table_name} (tokenLink, tokenName, symbol, price, dayDiff, mcap, liquidity, dayVolume, holders)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Выполнение команды внесения данных
        for tokenData in tokenList:
            cur.execute(sql, (
                tokenData['tokenLink'],
                tokenData['tokenName'],
                tokenData['symbol'],
                tokenData['price'],
                tokenData['dayDiff'],
                tokenData['mcap'],
                tokenData['liquidity'],
                tokenData['dayVolume'],
                tokenData['holders']
            ))
        base.commit()
        
    except Exception as e:
        print('Критическая ошибка с вносом новых токенов!', e)
        
        
def getLastTokenList():
    current_date = datetime.datetime.now()
    table_name = "day_" + current_date.strftime("%d%m%y")
    
    try:
        cur.execute(f'SELECT tokenLink FROM {table_name}')
        lastTokenList = cur.fetchall()
        newTokenList = [tokenLink[0] for tokenLink in lastTokenList]
        
        return newTokenList[-50:]

    except Exception as e:
        print('Произошла ошибка с получением предыдущего списка токенов', e)    
        
def sqlGetUserIds():
    try:
        cur.execute(f'SELECT userID FROM users')
        users = cur.fetchall()
        return users
    
    except Exception as e:
        print('Произошла ошибка с получением айди пользователей', e)   
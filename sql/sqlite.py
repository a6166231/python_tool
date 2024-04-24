from enum import Enum
import sqlite3
from typing import Any

import sys,os

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

DB_PATH = './whwPy.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

class SQLDataType(Enum):
    TEXT = 'TEXT'
    NUMBER = 'NUMBER'
    BOOL = 'BOOL'

def execute(cmd):
    try:
        cursor.execute(cmd)
    except Exception as e:
        print(e)
        conn.rollback()
def close():
    conn.close()
    cursor.close()
def commit():
    try:
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def deleteTable(tableName: str):
    execute(f'DROP TABLE IF EXISTS {tableName}')

def createTable(tableName: str, keyObj: dict[str, SQLDataType]):
    keys = []
    for k in keyObj:
        keys.append(f'{k} {keyObj[k].value}')
    execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({','.join(keys)})")

def insertIntoTable(tableName: str, value: dict[str, Any]):
    val = []
    for k in value:
        val.append(f"'{value[k]}'")
    execute(f"INSERT INTO {tableName} VALUES ({','.join(val)})")
    commit()

def deleteFromTable(tableName: str, where: str = ''):
    whereCMD = ''
    if len(where) != 0:
        whereCMD = f' WHERE {where}'
    execute(f"DELETE FROM {tableName} {whereCMD}")
    commit()

def selectFromTable(talbeName: str, key: str = '*', where: str = ''):
    whereCMD = ''
    if len(where) != 0:
        whereCMD = f' WHERE {where}'
    execute(f"SELECT {key} FROM {talbeName} {whereCMD}")
    return cursor.fetchall()

# deleteTable('games')
# createTable('games', {
#     "name": SQLDataType.TEXT,
#     # "time": SQLDataType.TEXT,
#     "difficulty": SQLDataType.NUMBER,
#     "online": SQLDataType.BOOL
# })

# gameData = [
#     {'name': '游戏1', 'difficulty': 1, 'online': False},
#     {'name': '游戏2', 'difficulty': 2, 'online': True},
# ]

# for g in gameData:
#     insertIntoTable('games', g)

result = selectFromTable('games', '*', "online>0")
print(result)
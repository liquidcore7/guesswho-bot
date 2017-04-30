import sqlite3, requests
from random import randint
from io import StringIO

def start():
    handler = sqlite3.connect('images.db')
    handler.execute("CREATE TABLE IF NOT EXISTS actors ("
                    "id INTEGER PRIMARY KEY,"
                    "local INTEGER, adress BLOB, name TEXT);")
    handler.commit()
    return handler

def getrow(handler, index, row) :
    lc = handler.execute("SELECT {0} FROM actors WHERE id={1}".format(row, index)).fetchone()
    return lc[0]

def local(handler, index):
    lc = getrow(handler, index, 'local')
    return True if lc == 1 else False

def randinex(handler):
    last = len(handler.cursor().execute("SELECT * FROM actors").fetchall())
    return randint(1, last)

def getonlineimage(url):
    return requests.get(url=url)

def start_game():
    handler = start()
    ind = randinex(handler)
    names = getrow(handler, ind, 'name')
    if local(handler, ind):
        return (getrow(handler, ind, 'adress'), handler, names)
    else:
        tfilename = "{}.jpg".format(getrow(handler, ind, 'name').split(',')[0])
        with open(tfilename, 'wb') as f:
            f.write(getonlineimage(getrow(handler, ind, 'adress')).content)
            f.close()
        return (tfilename, handler, names)
import sqlite3
import re

def bd():
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS Users(user_id INTEGER NOT NULL PRIMARY KEY,'
				'status INTEGER DEFAULT 0 NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS Channels(channel_id INTEGER PRIMARY KEY NOT NULL,'
				'user_id INTEGER REFERENCES Users (user_id) NOT NULL)')


async def key_writer(link):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	mass = []
	mass.append(link)
	cur.execute('INSERT INTO SDAKeys VALUES(?)', mass)
	con.commit()
	cur.close()

async def get_sdkey():
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('SELECT * FROM SDAKeys')
	data = cur.fetchall()
	key = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	cur.close()
	return key

async def delete_sdkey(key):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'DELETE FROM SDAKeys WHERE key = \'{key}\'')
	con.commit()
	cur.close()

async def add_user(id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	mass = []
	mass.append(id)
	cur.execute('INSERT OR IGNORE INTO USERS(user_id) VALUES(?)', mass)
	con.commit()
	cur.close()

async def add_channel(channel_id, user_id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('INSERT OR IGNORE INTO CHANNELS(channel_id, user_id) VALUES('+channel_id+','+user_id+')')
	con.commit()
	cur.close()


async def user_get_status(id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'SELECT status FROM Users WHERE user_id = {id}')
	data = cur.fetchall()
	status = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	cur.close()
	return status


async def user_set_status(status, id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'UPDATE Users SET status = {status} WHERE user_id = {id}')
	con.commit()
	cur.close()
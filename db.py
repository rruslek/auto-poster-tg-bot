import sqlite3
import re


def bd():
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS Users(user_id INTEGER NOT NULL PRIMARY KEY,'
				'status INTEGER DEFAULT 0 NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS Channels(channel_id INTEGER PRIMARY KEY NOT NULL,'
				'user_id INTEGER REFERENCES Users (user_id) NOT NULL,'
				'channel_name TEXT NOT NULL,'
				'channel_link TEXT)')
	cur.execute('CREATE TABLE IF NOT EXISTS Posts(post_id INTEGER PRIMARY KEY NOT NULL,'
				'channel_id INTEGER REFERENCES Channels (channel_id) NOT NULL,'
				'post_caption TEXT NOT NULL,'
				'post_media TEXT,'
				'post_date DATETIME NOT NULL)')


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


async def add_channel(user_id, channel_id, channel_name, channel_link):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('INSERT OR IGNORE INTO CHANNELS(user_id, channel_id, channel_name, channel_link) '
				'VALUES(?,?,?,?)',
				(user_id, channel_id, channel_name, channel_link))
	con.commit()
	cur.close()


async def add_post(channel_id, post_caption, post_media, post_date):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute('INSERT OR IGNORE INTO POSTS(post_id, channel_id, post_caption, post_media, post_date) '
				'VALUES(NULL,?,?,?,?)',
				(channel_id, post_caption, post_media, post_date))
	con.commit()
	cur.close()


async def get_posts(id, date_start, date_end):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'SELECT * FROM Posts WHERE channel_id = {id} '
				f'AND post_date > \"{date_start}\" AND post_date < \"{date_end}\"'
				f'ORDER BY post_date ASC')
	data = cur.fetchall()
	#status = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	cur.close()
	return data


async def get_post_content(post_id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'SELECT * FROM Posts WHERE post_id = {post_id} ')
	data = cur.fetchall()
	#status = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	cur.close()
	return data[0]

async def user_get_channels(id):
	con = sqlite3.connect("AutoPosterTG.db")
	cur = con.cursor()
	cur.execute(f'SELECT * FROM Channels WHERE user_id = {id}')
	data = cur.fetchall()
	#status = re.sub('|\(|\'|\,|\)', '', str(data[0]))
	cur.close()
	return data


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
import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://www.theverge.com/"
headers = {'User-Agent':'Mozilla/5.0'}
def scrape(db):
	html = requests.get(url,headers=headers).content
	soup = BeautifulSoup(html,"html.parser")
	conn = db.connect()
	if conn is not None:
		for i in reversed(soup.find_all('h2', class_='c-entry-box--compact__title')): 
			try :
				j = i.find('a')
				c = conn.cursor()
				c.execute("INSERT INTO content_agg(source,title,url) VALUES('theverge', ?, ?)",(j.text.strip(), j['href']))
			except sqlite3.IntegrityError as e:
				pass
			except Exception as e:
				print("Error : ", e)
				return False
		conn.commit()
		conn.close()
		return True
	else :
		return False
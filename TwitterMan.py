from bs4 import BeautifulSoup as bs
import urllib
import sys
#import got-python

#This function return tweets from
#given username's account as a list
def get_tweets(username):
	tweets = []
	

	URL = "https://twitter.com/"+username
	soup = bs(urllib.request.urlopen(URL), 'lxml')

	for li in soup.find_all("li", class_='js-stream-item'):
		text_p = li.find("p", class_="tweet-text")
		if text_p is not None:
			tweets.append(text_p.get_text())
	return tweets
	

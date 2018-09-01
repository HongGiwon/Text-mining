# Project	: Text Mining (CS474)
# Task 		: Web Crawling (reply)
# Name 		: reply_craw.py
# Creater 	: Giwon Hong
# Date 		: 2018.08.31

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

r=requests.get('https://search.joins.com/JoongangNews?page=1&Keyword=%EA%B9%80%EC%98%81%EB%9E%80&PeriodType=DirectInput&StartSearchDate=01%2F01%2F2006%2000%3A00%3A00&EndSearchDate=09%2F01%2F2018%2000%3A00%3A00&SortType=New&SearchCategoryType=JoongangNews')
c=r.content

be_c = BeautifulSoup(c, "html.parser")

div_searchlist_num = be_c.find("span",{"class":"total_number"}).text.split(' / ')[0].split('-')[1]

#div_search_news_list = be_c.find("ul",{"class":"list_default"})

print(div_searchlist_num)

errorlist = []

for search_index in range(1,(int(div_searchlist_num)+1)):

	try:
		if (search_index % 10 == 0):
			print(str(search_index) + ':' + str(int(div_searchlist_num)+1))

		next_page_list_html=requests.get('https://search.joins.com/JoongangNews?page=' + str(search_index) + '&Keyword=%EA%B9%80%EC%98%81%EB%9E%80&PeriodType=DirectInput&StartSearchDate=01%2F01%2F2006%2000%3A00%3A00&EndSearchDate=09%2F01%2F2018%2000%3A00%3A00&SortType=New&SearchCategoryType=JoongangNews')
		next_page_list = next_page_list_html.content
		be_next_page_list = BeautifulSoup(next_page_list, "html.parser")
		div_search_news_list = be_next_page_list.find("ul",{"class":"list_default"})

		for div_search_news in div_search_news_list.find_all("li"):
			div_search_news_meta = div_search_news.find("span",{"class":"byline"}).find_all("em")
			div_search_news_comp = div_search_news_meta[0].text
			div_search_news_date = div_search_news_meta[1].text

			div_search_news_link = div_search_news.find("strong",{"class":"headline mg"}).find("a")['href']

			dirname = './result_reply2/' + str(div_search_news_date[:4])
			filepath_full = dirname + "/"+str(div_search_news_link.split('article/')[1])+".txt"
			if (os.path.isfile(filepath_full)):
				continue

			driver = webdriver.Chrome('E:/텍마/chromedriver.exe')
			driver.get(div_search_news_link)
			news_page_html = driver.page_source

			be_news_page = BeautifulSoup(news_page_html, features="html.parser")

			div_news_page_comment = be_news_page.find("div",{"class":"comment_area"})
			div_news_page_comment_list = div_news_page_comment.find("div",{"class":"comment_list"})



			if not (div_news_page_comment_list is None):

				#if not os.path.isdir(dirname):
				#	os.mkdir(dirname)

				comment_save_list = []
				for comment in div_news_page_comment_list.find_all("li"):
					comment_save_list.append(comment.find("p",{"class":"content"}).text)

				if (len(comment_save_list) > 0):
					with open(dirname + "/"+str(div_search_news_link.split('article/')[1])+".txt", 'w', encoding="utf-8" ) as f:
						for comment in comment_save_list:
							f.write(comment + '\n')

			driver.stop_client()
			driver.close()

	except:
		print(str(search_index) + ':' + str(int(div_searchlist_num)+1))
		print("error:" + str(search_index))
		errorlist.append(search_index)
		continue

print("error list :")
print(errorlist)
'''
driver = webdriver.Chrome('E:/텍마/chromedriver.exe')
driver.get('https://news.joins.com/article/22922950')

html = driver.page_source

be_news_page = BeautifulSoup(html, features="html.parser")

div_news_page_comment = be_news_page.find("div",{"class":"comment_area"})
div_news_page_comment_list = div_news_page_comment.find("div",{"class":"comment_list"})

for comment in div_news_page_comment_list.find_all("li"):
	print(comment.find("p",{"class":"content"}).text)
	break
'''
# Project	: Text Mining (CS474)
# Task 		: Web Crawling
# Name 		: craw.py
# Creater 	: Giwon Hong
# Date 		: 2018.08.31

import os
import requests
from bs4 import BeautifulSoup

r=requests.get('https://search.joins.com/TotalNews?page=1&Keyword=%EA%B3%B5%EB%AC%B4%EC%9B%90&PeriodType=DirectInput&StartSearchDate=01%2F01%2F2006%2000%3A00%3A00&EndSearchDate=08%2F31%2F2018%2000%3A00%3A00&SortType=New&SearchCategoryType=TotalNews')
c=r.content

be_c = BeautifulSoup(c, "html.parser")

div_searchlist_num = be_c.find("span",{"class":"total_number"}).text.split(' / ')[0].split('-')[1]

#div_search_news_list = be_c.find("ul",{"class":"list_default"})

print(div_searchlist_num)

errorlist = []

for search_index in range(1,(int(div_searchlist_num)+1)):

	try:
		if (search_index % 100 == 0):
			print(str(search_index) + ':' + str(int(div_searchlist_num)+1))

		next_page_list_html=requests.get('https://search.joins.com/TotalNews?page=' + str(search_index) + '&Keyword=%EA%B3%B5%EB%AC%B4%EC%9B%90&PeriodType=DirectInput&StartSearchDate=01%2F01%2F2006%2000%3A00%3A00&EndSearchDate=08%2F31%2F2018%2000%3A00%3A00&SortType=New&SearchCategoryType=TotalNews')
		next_page_list = next_page_list_html.content
		be_next_page_list = BeautifulSoup(next_page_list, "html.parser")
		div_search_news_list = be_next_page_list.find("ul",{"class":"list_default"})

		for div_search_news in div_search_news_list.find_all("li"):
			div_search_news_meta = div_search_news.find("span",{"class":"byline"}).find_all("em")
			div_search_news_comp = div_search_news_meta[0].text
			div_search_news_date = div_search_news_meta[1].text

			div_search_news_link = div_search_news.find("strong",{"class":"headline mg"}).find("a")['href']
			
			news_page_html = requests.get(div_search_news_link)
			news_page = news_page_html.content
			be_news_page = BeautifulSoup(news_page, "html.parser")

			div_news_page_contents = be_news_page.find("div",{"class":"article_body"}).text

			dirname = './result/' + div_search_news_comp
			if not os.path.isdir(dirname):
				os.mkdir(dirname)

			dirname = './result/' + div_search_news_comp + '/' + str(div_search_news_date[:4])
			if not os.path.isdir(dirname):
				os.mkdir(dirname)

			with open(dirname + "/"+str(div_search_news_link.split('article/')[1])+".txt", 'w', encoding="utf-8" ) as f:
				f.write(str(div_search_news_comp) + '\n')
				f.write(str(div_search_news_date) + '\n')
				f.write(div_news_page_contents)

	except:
		print(str(search_index) + ':' + str(int(div_searchlist_num)+1))
		print("error:" + str(search_index))
		errorlist.append(search_index)
		continue

print("error list :")
print(errorlist)
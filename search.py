# Project	: Text Mining (CS474)
# Task 		: Article anaysis (keywords)
# Name 		: search.py
# Creater 	: Giwon Hong
# Date 		: 2018.08.31

import os

dictfilelist = {}
def txtsearch(dirp):
	
	filelist = os.listdir(dirp)
	for file in filelist:
		filepath = os.path.join(dirp, file)
		if (os.path.isdir(filepath)):
			txtsearch(filepath)
		else:
			if (os.path.splitext(filepath)[-1] == '.txt'):
				seglist = filepath.split('\\')
				if not seglist[2] in dictfilelist:
					dictfilelist[seglist[2]] ={}
					dictfilelist[seglist[2]][seglist[1]] = [filepath]
				elif not seglist[1] in dictfilelist[seglist[2]]:
					dictfilelist[seglist[2]][seglist[1]] = [filepath]
				else:
					dictfilelist[seglist[2]][seglist[1]].append(filepath)

txtsearch('./result')

countdict = {}

for years in dictfilelist:
	if not years in countdict:
		countdict[years] = 0
	for news in dictfilelist[years]:
		for path in dictfilelist[years][news]:

			with open(path, 'r', encoding="utf-8" ) as f:
				contents = f.readlines()
				for con in contents[2:]:
					if not ((con.find('뇌물') == -1) and con.find('청탁') == -1 and con.find('촌지')==-1 and con.find('금품')==-1 and con.find('향응') == -1 and con.find('수뢰') == -1 and con.find('증뢰') == -1):
						if not ((con.find('범죄') == -1) and con.find('입건') == -1 and con.find('구속')==-1 and con.find('처벌')==-1 and con.find('혐의') == -1 and con.find('체포') == -1 and con.find('선고') == -1):
							if (con.find('부정청탁 및 금품등 수수의 금지') == -1):
								countdict[years] += 1

print(countdict)

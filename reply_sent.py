# Project	: Text Mining (CS474)
# Task 		: Sentiment analysis (reply)
# Name 		: reply_sent.py
# Creater 	: Giwon Hong
# Date 		: 2018.08.31


import os
from google.cloud import language
from google.cloud.language import enums as lan_enums
from google.cloud.language import types as lan_types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project-f557b58c64ab.json'
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
				if not seglist[1] in dictfilelist:
					dictfilelist[seglist[1]] = [filepath]
				else:
					dictfilelist[seglist[1]].append(filepath)

def sen_analysis_value(input_text):
    client = language.LanguageServiceClient()
    document = lan_types.Document(
        content=input_text,
        type=lan_enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document).document_sentiment
    return sentiment.score

txtsearch('./result_reply2')

scoresumdict = {}
countdict = {}
count = 0

for years in dictfilelist:
	if not years in scoresumdict:
		scoresumdict[years] = 0
		countdict[years] = 0
	count = 0
	lenyear = len(dictfilelist[years])
	for path in dictfilelist[years]:
		if (count % 10 == 0):
			print(str(count) + ':' + str(lenyear) + ' year : ' + str(years))
		with open(path, 'r', encoding="utf-8" ) as f:
			contents = f.readlines()
			for con in contents:
				scoresumdict[years] += sen_analysis_value(con)
				countdict[years] += 1
		count += 1

print(scoresumdict)
print(countdict)

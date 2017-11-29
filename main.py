import os.path,sys,os
DICT_FILE = open("dict","r")
line = DICT_FILE.readline()
dict = {}
while line:
	line = line.strip('\n')
	print(line)
	a = line.split(':')
	if(len(a)==2):
		dict[a[0]] = a[1]
	line = DICT_FILE.readline()
DICT_FILE.close()

def hash(path):
	import hashlib
	md5file=open(path,'rb')
	md5=hashlib.md5(md5file.read()).hexdigest()
	md5file.close()
	return(md5)
	
hash_dict = {}

HASH_FILE = open("hash","r")
line = HASH_FILE.readline()
dict = {}
while line:
	line = line.strip('\n')
	print(line)
	a = line.split(':')
	if(len(a)==2):
		hash_dict[a[0]] = a[1]
	line = HASH_FILE.readline()
HASH_FILE.close()



print(hash_dict)					
print("Uploaded")

from wxpy import *

from tempfile import NamedTemporaryFile
import time
import random

bot = Bot(cache_path=True)
# bot.logout()
tuling = Tuling(api_key='')

def retry(msg,t = 0):
	flag = 0
	try:
		url = emotions_reply(msg.text[5])
		if url =='':
			msg.reply("[不支持的图片应答]")
			flag = -1
			return flag
		res = requests.get(url,allow_redirects=False)
		cur = str(int(time.time()*1000)) + url[-4:]
		tmp = open(cur,'wb')
		tmp.write(res.content)
		print(tmp.name)
		n = 0
		while n<5:
			try:
				media_id = bot.upload_file(cur)
				msg.reply_image('',media_id)
				n = 5
				flag = 1
			except Exception as e:
				print("try" + str(n) + '\t' + e)
				n+=1
			
		tmp.close()
	except:
		msg.reply("我死机啦")
		if t<3:
			print("Retry "+str(t))
			retry(msg,t+1)


@bot.register()
def auto_reply(msg):
	if not isinstance(msg.chat, Group):
		print(msg.type)
		if msg.type == 'Picture':
			path = msg.file_name
			print(path)
			try:
				msg.get_file(save_path=path)
			except Exception as e:
				print(e)
				
			if os.path.getsize(path) != 0:
				md5 = hash(path)
				if md5 not in hash_dict:
					try:
						media_id = bot.upload_file(path)
						hash_dict[md5] = media_id
						HASH_FILE = open("hash","ab")
						HASH_FILE.write((md5+':'+media_id+'\n').encode('gb2312'))
						HASH_FILE.close()
					except:
						print("Upload Error")	
			element = hash_dict[random.choice(list(hash_dict))]
			if element != None:
				msg.reply_image('.gif',element)
			
		elif msg.type == 'Text' and len(msg.text)> 5 and msg.text[:5]=='@pic@':
			flag = 0
			try:
				url = emotions_reply(msg.text[5])
				if url =='':
					msg.reply("[不支持的图片应答]")
					flag = -1
					return flag
				res = requests.get(url,allow_redirects=False)
				cur = str(int(time.time()*1000)) + url[-4:]
				tmp = open(cur,'wb')
				tmp.write(res.content)
				print(tmp.name)
				n = 0
				while n<5:
					try:
						media_id = bot.upload_file(cur)
						msg.reply_image('',media_id)
						n = 5
						flag = 1
					except Exception as e:
						print("try" + str(n) + '\t' + e)
						n+=1
					
				tmp.close()
			except:
				pass
			if not flag:
				print("Unknown Bug, Retry")
				retry(msg)
				
		elif msg.type == 'Text' and msg.text!='' and msg.text[0]=='=' and msg.text.find(':')!=-1:
			print("000" + msg.text)
			sp = msg.text.strip('=').split(':')
			
			try:
				DICT_FILE = open("dict","ab")
				DICT_FILE.write((msg.text.strip('=')+'\n').encode('gb2312'))
				DICT_FILE.close()
				print("write = " + msg.text.strip('='))
			except:
				print("OMG\n")
			dict[sp[0]] = sp[1]
			msg.reply(r"我学会了 "+ sp[0] +" 的应答语是 " + sp[1])
		elif msg.type == 'Text' and msg.text in dict:
			print(msg.text)
			msg.reply(dict[msg.text])
		else:
			if msg.type == 'Text' and msg.type != 'Sharing':
				print(msg.text)
				tuling.do_reply(msg)
			else:
				msg.reply("我死机了")
				
import requests
from lxml import etree
import random
def emotions_reply(keyword):
	print("try gif reply...")
	res = requests.get('https://www.doutula.com/search', {'keyword': keyword})
	html = etree.HTML(res.text)
	urls = html.xpath('//*[@id="search-result-page"]/div/div/div[2]/div/div[1]/div/div/a/img/@data-original')
	if len(urls) < 1:
		raise Exception('doutula cannot reply this message')
	url = random.choice(urls)
	print(url)
	return url


embed()


# cyf = ensure_one(bot.search(u'xxx'))
# @bot.register(cyf)
# def reply_my_friend(msg):
	# tuling.do_reply(msg)
# embed()


# @bot.register()
# def auto_reply(msg):
	# # 如果是群聊，但没有被 @，则不回复
	# if isinstance(msg.chat, Group) and msg.is_at or isinstance(msg.chat, Friend):
		# tuling.do_reply(msg)
# embed()

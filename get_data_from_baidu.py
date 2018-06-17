# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json

original_url = "https://www.baidu.com/s?ie=utf-8&tn=baidu&wd={}&pn={}" # nojs=1
# "红客联盟 先调任杂志社任主编" 亮仔 蓝溪 冰刀 uhhuhy 蝶起 黑夜隐士 墨斗 仙儿 孤狼 SuperM
# original_keyword = "红客联盟 {}"
original_keyword = "绿色兵团 {}"

# gcp zone
# gcloud config set compute/zone asia-east1

# Data Structure would be
# page_rank_result = {"keyword":{1:[_referer_, url1, url2...,url10], 2:[url1, url2...url10]..., 10:[]}}
# 
page_rank_result = {}

def get_page_content(url, before_url=""):
	print("Checking URL [{}]...".format(url))
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0',
		'referer': before_url.encode("utf-8")
		# 'referer': before_url
	}
	baidu_page = requests.get(url, headers=headers)
	soup = BeautifulSoup(baidu_page.text, "html.parser")
	return soup

def check_baidu_rank(keyword):
	checking_url = original_url.format(keyword, 0)
	soup = get_page_content(checking_url, "https://www.baidu.com/baidu.html?from=noscript")
	before_url = checking_url
	page_rank_result[keyword][1] = [checking_url]
	get_baidu_page_results(1, soup, keyword)
	baidu_single_page = check_baidu_rank_task(soup)
	checking_url_num = 0
	before_checking_url_num = 0
	while (len(baidu_single_page) == 10 or checking_url_num < 990):
		baidu_page_num = int(baidu_single_page[-1].text) if len(baidu_single_page)!=0 else 1
		checking_url_num = (baidu_page_num-1)*10
		checking_url = original_url.format(keyword, str(checking_url_num))
		soup = get_page_content(checking_url, before_url)
		# save search results
		page_rank_result[keyword][baidu_page_num] = [checking_url]
		get_baidu_page_results(baidu_page_num, soup, keyword)
		if (checking_url_num <= before_checking_url_num):
			break
		before_url = original_url.format(keyword, str(before_checking_url_num))
		baidu_single_page = check_baidu_rank_task(soup)
		before_checking_url_num = checking_url_num
	return checking_url_num

def check_baidu_rank_task(soup):
	# pc should increase like 0->90->130->170->210 ...
	baidu_links = soup.find_all("span", class_="pc")
	time.sleep(2+2*random.random())
	return baidu_links

def get_baidu_page_results(cur_num, soup, keyword):
	print("Saving search result {} at {}".format(keyword, str(cur_num)))
	baidu_results = soup.find_all("div", class_="c-container")
	for r in baidu_results:
		baidu_result = [r.find_all("a")[0].get("href"), r.find_all("a")[0].text, baidu_article_content(r)]
		page_rank_result[keyword][cur_num].append(baidu_result)

def baidu_article_content(soup):
	abstract_tag = soup.find_all(class_="c-abstract")
	if len(abstract_tag) != 0:
		return abstract_tag[0].text
	span18_tag = soup.find_all(class_="c-span-last")
	if len(span18_tag) != 0:
		return span18_tag[0].text
	return ""

def additional_baidu_article(keyword):
	baidu_num_result = list(page_rank_result[keyword].keys())
	baidu_num_result.sort()
	print(baidu_num_result)
	last_num = baidu_num_result[-1]
	remaininig_num = list(set(range(1, last_num+1))-set(baidu_num_result))
	print(remaininig_num)
	before_url = "https://www.baidu.com/baidu.html?from=noscript"
	for i in remaininig_num:
		current_url = original_url.format(keyword, str((i-1)*10))
		soup = get_page_content(current_url, before_url)
		page_rank_result[keyword][i] = [current_url]
		get_baidu_page_results(i, soup, keyword)
		before_url = current_url

def read_file_search_query():
	query_file = open("baidu_search_query2.txt", "r")
	file_content = query_file.read()
	file_content = file_content.replace("\n", ",")
	return file_content.split(",")

# import sys
# reload(sys)
# sys.setdefaultencoding("utf8")

search_queries = read_file_search_query()

for kwd in search_queries:
	search_keyword = original_keyword.format(kwd)
	page_rank_result[search_keyword] = {}
	baidu_page_num = check_baidu_rank(search_keyword)
	additional_baidu_article(search_keyword)

	print(page_rank_result[search_keyword][1][0])

	json_file = open("files/{}_baidu_result.json".format(search_keyword), "w")
	json.dump(page_rank_result, json_file, ensure_ascii=False, indent=4)

# use virustotal api to validate whether page is safe or not
# https://www.virustotal.com/vtapi/v2/url/scan with params['apikey', 'url']
# after that, retrieve returned json and check data.



# -*- coding: UTF-8 -*-

import requests
import json
from bs4 import BeautifulSoup

file_name = "红客联盟 bkbll"
# file_name = "红客联盟 馨儿"
# file_name = "红客联盟 蓝凌"

def get_page_content(url, before_url=""):
	print("Checking URL [{}]...".format(url))
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0',
		'referer': before_url.encode("utf-8")
		# 'referer': before_url
	}
	try:
		baidu_page = requests.get(url, headers=headers, timeout=5)
	except requests.exceptions.RequestException as e:
		print("\nError occurs!\n")
		return ""
	# soup = BeautifulSoup(baidu_page.text, "html.parser")
	return baidu_page

def open_and_load_json(file_path):
	file_content = open(file_path, 'r')
	json_content = json.load(file_content)
	return json_content

def requests_and_get_url_and_data(file_path):
	json_content = open_and_load_json(file_path)
	keyword_content = json_content[file_name]
	k_result = {file_name:{}}
	for (k_key, k_lists) in keyword_content.items():
		k_referer = k_lists[0]
		k_result[file_name][k_key] = []
		for k_content in k_lists[1:]:
			k_page = get_page_content(k_content[0], k_referer)
			if k_page != "":
				k_result[file_name][k_key].append([k_page.url, k_page.text])
				print(k_page.url)
	return k_result

# import sys
# reload(sys)
# sys.setdefaultencoding("utf8")

keyword_file_path = "files/{}_baidu_result.json".format(file_name)
keyword_result = requests_and_get_url_and_data(keyword_file_path)
keyword_search_file_path = "files/search_result_files/{}_baidu_result.json".format(file_name)
search_result_json = open(keyword_search_file_path, "w")
json.dump(keyword_result, search_result_json, ensure_ascii=False, indent=4)



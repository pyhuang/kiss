#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

URL_PREFIX = "http://www.kiss.com.tw"

class Kiss:
	def __init__(self):
		self.update()

	def update(self):
		args = {'area':'0'}
		response = requests.get(URL_PREFIX + '/templates/header_songlist_json.php', params=args) 
		self._raw = response.content.decode('unicode_escape') 
		
	def raw_data(self):
		return self._raw

	def time(self):
		com_time = re.compile('[0-9]{2}:[0-9]{2}')
		time = com_time.search(self._raw)

		if time:
			return time.group()
		else:
			return str()
		
	def singer(self):
		data = re.sub('<\\\/a>', '', re.sub('<a .*?>', '', self._raw))
		com_singer = re.compile('(?<=：).*?(?= - )')
		singer = com_singer.search(data)

		if singer:
			return singer.group()
		else:
			return str()

	def artist_url(self):
		com_have_url = re.compile('(?<=：).*?(?=<\\\/a>)')
		have_url = com_have_url.search(self._raw)

		if have_url:
			com_url = re.compile('(?<=href=").*?(?=">)')
			url = com_url.search(have_url.group())
			return URL_PREFIX + url.group().replace("\/","/")
		else:
			return str()

	def song(self):
		data = re.sub('<\\\/a>', '', re.sub('<a .*?>', '', self._raw))
		com_song = re.compile('(?<= - ).*?(?="})')
		song = com_song.search(data)
		if song:
			return song.group()
		else:
			return str()
		
	def album_url(self):
		com_have_url = re.compile('(?<= - <a).*?(?=<\\\/)')
		have_url = com_have_url.search(self._raw)

		if have_url:
			com_url = re.compile('(?<=href=").*?(?=">)')
			url = com_url.search(have_url.group())
			return URL_PREFIX + url.group().replace("\/","/")
		else:
			return str()
		
if __name__ == '__main__':

	kiss = Kiss()
	print(kiss.time() + " / " + kiss.singer() + " / " + kiss.song())

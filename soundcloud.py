#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, string, time
import json
import urllib

__author__ = 'DaRealFreak'
__date__ = 'Mon August 05 05:41:06 2013'
__doc__ = 'simple soundcloud downloader using the widget of soundcloud.com'

class SoundCloud(object):
	"""
	simple class for directly downloading artists pages or track lists from soundcloud.com
	"""

	VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
	DOWNLOAD_FOLDER = 'Music'
	log = False
	
	class OperaURLopener(urllib.FancyURLopener):
		"""
		AppUrlOpener based on this example of the official python documentation:
		http://docs.python.org/2/library/urllib.html
		"""
		version = "Opera/9.80 (Windows NT 6.1; U; us-US) Presto/2.7.62 Version/11.01"	
		
	def __init__(self):
		os.system("clear") if sys.platform in ('linux', 'linux2') else os.system("cls")
		url = raw_input('track to soundcloud url:\n')
		self._download_page(url)
	
	def __reporthook(self, blocks_read, block_size, total_size):
		# clean the system line and 'updating' our status
		sys.stdout.write("\r% 3.1f%% of %d bytes "
			% (float(blocks_read * block_size) / total_size * 100, total_size))
		sys.stdout.flush()

	def _download_file(self, data):
		# parsing the data dictionary to retrieve the streaming url and create a valid file path
		stream_url = data['stream_url']
		file_path = os.path.join(os.getcwd(), self.DOWNLOAD_FOLDER, ''.join(char for char in data['title'] + ".mp3" if char in self.VALID_CHARS))
		
		sys.stdout.write('\ntrying to retrieve remote %s to local %s\n' % (stream_url, file_path))

		# to prevent overwriting existing files, just ignore them
		if not os.path.exists(file_path):
			(file_name, headers) = urllib.urlretrieve(stream_url, file_path, self.__reporthook)
			if self.log:
				sys.stdout.write("(filename: %s, headers: %s)\n" % (file_name, headers))	

	def _download_page(self, url):
		# initializing our url variable
		url = "http://soundcloud.com/widget.json?" + urllib.urlencode(
			{
				'url':url
			})
			
		# using a new AppUrlOpener, based on this exampes(http://docs.python.org/2/library/urllib.html)
		urllib._urlopener = self.OperaURLopener()
		# read the widget and parse it using json
		widget = urllib.urlopen(url).read()
		data = json.loads(widget)
		
		if not os.path.isdir(os.path.join(os.getcwd(), self.DOWNLOAD_FOLDER)):
			os.makedirs(os.path.join(os.getcwd(), self.DOWNLOAD_FOLDER))
		
		# 'tracks' is in the keys if an artist page or track-list is opened
		if 'tracks' in data.keys():
			# retrieve for every track in the track-list the data
			[self._download_file(track) for track in data['tracks']]
		else:
			# if only one track is opened retrieve this one
			self._download_file(data)

if __name__ == "__main__":
	SoundCloud()

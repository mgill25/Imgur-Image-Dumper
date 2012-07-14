#!/usr/bin/python
# Python script to download complete albums from imgur.
# Currently only working in blog layout, displaying all the images on a single page.
import requests
from bs4 import BeautifulSoup
import os, errno
import sys
# import logging

class Dumper(object):
	urls = []

	def get_images(self, url, headers):
		""" Collect all the urls, iterate over them, downloading every one.""" 
		res = requests.get(url=url, headers=headers)
	
		if not res.status_code == requests.codes.ok:			
			raise res.raise_for_status()

		content = res.content
		soup = BeautifulSoup(content)
		link_tags = soup.findChildren(attrs={'class':'item view album-view-image-link'})
		
		for elem in link_tags:
			url = elem.find('a').get('href')					
			self.urls.append(url)	

		folder = 'Imgur_Album'

		# if not os.path.exists(folder):
		# 	os.makedirs(folder)			# mkdir -p
		# The above way is bad, because a dir can be created between the 2 function calls, thus causing a race condition
		
		# better way:
		try:
			os.makedirs(folder)
		except OSError, e:
			if e.errno == errno.EEXIST:
				print "Directory Already exists."
				print "Download to existing directory?"
				input = raw_input("[y/n]")
				if not input.lower() == 'y':
					print "Rename, or modify the directory name in the program."
					sys.exit()

		count = 0	# name files according to count. 1.jpg, 2.jpg etc...

		for elem in self.urls:
			print 'Downloading %s ' %(elem)
			try:
				image_ = requests.get(elem)				
				if not image_.status_code == requests.codes.OK:
					raise image_.raise_for_status()			
			except Exception as e:
				print " %s: %s" %(type(e), str(e))
			else:
				image_data = image_.content
				file_name = folder + '/' + str(count + 1) + os.path.splitext(elem)[1]
				fsock = open(file_name, 'wb')
				fsock.write(image_data)
				count += 1

		print "Done! :)"

def main():
	album_url = 'http://imgur.com/a/vw7Q1/layout/blog'	
	headers = {'Accept':'text/css,*/*;q=0.1',
	'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip,deflate,sdch',
	'Accept-Language':'en-US,en;q=0.8',
	'User-Agent':'Mozilla/5 (Solaris 10) Gecko'}

	d = Dumper()
	try:
		d.get_images(album_url, headers)
	except Exception as e:
		print "Sorry, an error occured. This could be due to a bad link.\nError: %s: %s" %(type(e), str(e))

if __name__ == '__main__':
	sys.exit(main())

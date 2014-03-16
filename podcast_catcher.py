# --coding:utf-8 --#
"""Podcast Catcher

Catch mp3 file of specified podcast

Usage:
	python podcast_catcher.py [options] [source]

Options:
	-h			show help doc
	-s ...			specified source, include esl, tps and gg now
	-a			catch all available source
	-p ...			specified proxy
	-l ...			specified link

Sources:
	esl
	tps
	gg
	mix
	tcl

Examples:
	podcast_catcher -s esl			catch latest esl
	podcast_catcher -a -p http://example.com:8080			catch all by using example.com:8080 as proxy

"""
	
import urllib2
import sys
import getopt
import re
import time

class Catcher():
	def __init__(self, proxy, url = ''):
		proxy_handler = urllib2.ProxyHandler({'http' : proxy})
		self.opener = urllib2.build_opener(proxy_handler)
		f = self.opener.open(url)
		self.content = f.read()
		
	def download(self):
		self.parser()	#MAKE THEM CLEARLY!!!
		request = urllib2.Request(self.link)
		data = self.opener.open(request).read()
		f = file(self.link.split('/')[-1], 'wb')
		f.write(data)
		f.close
		print 'Complete.'

	def parser(self):
		pass

class ESL_Catcher(Catcher):
	def __init__(self, proxy, url = 'http://www.eslpod.com/website/index_new.html'):
		Catcher.__init__(self, proxy, url)	#why is not *super*???
		#super(ESL_Catcher, self).__init__(self, proxy)

	def parser(self):
		end = self.content.find('.mp3') + 4
		start = self.content.rfind('http', 0, end)
		self.link = self.content[start : end]
		print self.link

class TPS_Catcher(Catcher):
	def __init__(self, proxy, url = 'http://publicspeaker.quickanddirtytips.com/'):
		Catcher.__init__(self, proxy, url)

	def parser(self):
		end = self.content.find('.mp3') + 4
		end = self.content.find('.mp3', end) + 4
		start = self.content.rfind('http', 0, end)
		self.link = self.content[start : end]
		print self.link

class GG_Catcher(Catcher):
	def __init__(self, proxy, url = 'http://grammar.quickanddirtytips.com/'):
		Catcher.__init__(self, proxy, url)

	def parser(self):
		end = self.content.find('.mp3') + 4
		end = self.content.find('.mp3', end) + 4
		start = self.content.rfind('http', 0, end)
		self.link = self.content[start : end]
		print self.link

class MIX_Catcher(Catcher):
	def __init__(self, proxy, url = 'http://mixergy.com/'):
		Catcher.__init__(self, proxy, url)

	def parser(self):
		return "hi"

class TCL_Catcher(Catcher):
	def __init__(self, proxy, url = 'http://5by5.tv/changelog'):
		Catcher.__init__(self, proxy, url)

	def parser(self):
		pattern = '#(\d+):'	
		episode = re.search(pattern, self.content).group(1)
		self.content = self.opener.open('http://5by5.tv/changelog/'+episode).read()
		end = self.content.find('.mp3') + 4
		end = self.content.find('.mp3', end) + 4
		start = self.content.rfind('http', 0, end)
		self.link = self.content[start : end]
		print self.link

def usage():
	print __doc__

def main(argv):
	proxy  = 'http://127.0.0.1:8087'
	
	try:
		opts, args = getopt.getopt(argv, 'hs:p:a')
		for opt, arg in opts:
			if opt == 'h':
				usage()
				sys.exit()
			elif opt == '-s':
				source = arg
			elif opt == '-p':
				proxy == arg
			elif opt == '-a':
				pass
		
		import podcast_catcher
		approp_catcher = getattr(podcast_catcher, '%s_Catcher' % source.upper())
	except:
		usage()
		sys.exit()

	catcher = approp_catcher(proxy)
	#print catcher.link		#WHY CAN'T???
	start = time.clock()
	catcher.download()
	end = time.clock()
	print 'consume %ds' % (end - start)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		usage()
		sys.exit()
		
	main(sys.argv[1:])

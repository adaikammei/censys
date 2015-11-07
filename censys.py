#!/usr/bin/env python
#-*- coding: utf-8 -*-# Name:     nocommonssids.py
# Purpose:  CynsysIO API Script
# By:       Jerry Gamblin
# Date:     07.11.15
# Modified  07.11.15
# Rev Level 0.8
# -----------------------------------------------

from termcolor import colored
import argparse
import json
import requests
import codecs
import locale
import os
import sys
import ast

	
class Censys:

	def __init__(self, ip):

		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = "Get From Censys.IO"
		self.SECRET = "Get From Censys.IO"
		self.ip = ip

	def search(self):

		pages = float('inf')
		page = 1

		while page <= pages:  

			params = {'query' : self.ip, 'page' : page}
			res = requests.post(self.API_URL + "/search/ipv4", json = params, auth = (self.UID, self.SECRET))
			payload = res.json()
			

			for r in payload['results']:

				ip = r["ip"]
				proto = r["protocols"][0].replace(' ', '-')
				
		
			
				print '[%s] IP: %s - Protocols: %s' % (colored('*', 'red'), ip, proto)
				
				
				if '80/http' in proto:
					self.view(ip)

			pages = payload['metadata']['pages']
			page += 1

	def view(self, server):

		res = requests.get(self.API_URL + ("/view/ipv4/%s" % server), auth = (self.UID, self.SECRET))
		payload = res.json()		

		try:
			if 'title' in payload['80']['http']['get'].keys():
				print "[+] Title: %s" % payload['80']['http']['get']['title']
			if 'server' in payload['80']['http']['get']['headers'].keys():
				print "[+] Server: %s" % payload['80']['http']['get']['headers']['server']
		except Exception as error:
			print error
		print ""

parser = argparse.ArgumentParser(description = 'CENSYS.IO Web Server Search')
parser.add_argument('-f', '--find', help='CENSYS Search', required = True)


args = parser.parse_args()
ip = args.find

censys = Censys(ip)
censys.search()

#
#  CamdRAED - Converter
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#	<convert type="CamdRAED">Camd</convert>
# </widget>			
# Edit By RAED 16-04-2013

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import os


class CamdRAED(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 2000
		self.poll_enabled = True
		
	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		camd = ""
		serlist = None
		camdlist = None
		nameemu = []
		nameser = []
		if not info:
			return ""
		# TS-Panel
		if fileExists("/etc/startcam.sh"):
			try:
				for line in open("/etc/startcam.sh"):
					if line.find("script") > -1:
						return "%s" % line.split("/")[-1].split()[0][:-3]
			except:
				camdlist = None
		# VTI 	
		elif fileExists("/tmp/.emu.info"):
			try:
				camdlist = open("/tmp/.emu.info", "r")
			except:
				return None
		# BlackHole	
		elif fileExists("/etc/CurrentDelCamName"):
			try:
				camdlist = open("/etc/CurrentDelCamName", "r")
			except:
				return None
		# DE-OpenBlackHole	
		elif fileExists("/etc/BhCamConf"):
			try:
				camdlist = open("/etc/BhCamConf", "r")
			except:
				return None
		# Domica	
		elif fileExists("/etc/active_emu.list"):
			try:
				camdlist = open("/etc/active_emu.list", "r")
			except:
				return None
		# Egami	
		elif fileExists("/tmp/egami.inf","r"):
			lines = open("/tmp/egami.inf", "r").readlines()
			for line in lines:
				item = line.split(":",1)
				if item[0] == "Current emulator":
					return item[1].strip()
		#Pli
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				for line in open("/etc/init.d/softcam"):
					if line.find("echo") > -1:
						nameemu.append(line)
				camdlist = "%s" % nameemu[1].split('"')[1]
			except:
				pass
			try:
				for line in open("/etc/init.d/cardserver"):
					if line.find("echo") > -1:
						nameser.append(line)
				serlist = "%s" % nameser[1].split('"')[1]
			except:
				pass
			if serlist is None:
				serlist = ""
			elif camdlist is None:
				camdlist = ""
			elif serlist is None and camdlist is None:
				serlist = ""
				camdlist = ""
			return ("%s %s" % (serlist, camdlist))
		# OoZooN
		elif fileExists("/tmp/cam.info"):
			try:
				camdlist = open("/tmp/cam.info", "r")
			except:
				return None
		# Dream Elit
		elif fileExists("/usr/bin/emuactive"):
			try:
				camdlist = open("/usr/bin/emuactive", "r")
			except:
				return None
		# Merlin2	
		elif fileExists("/etc/clist.list"):
			try:
				camdlist = open("/etc/clist.list", "r")
			except:
				return None
		# GP3
		elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
			try:
				from Plugins.Bp.geminimain.plugin import GETCAMDLIST
				from Plugins.Bp.geminimain.lib import libgeminimain
				camdl = libgeminimain.getPyList(GETCAMDLIST)
				cam = None
				for x in camdl:
					if x[1] == 1:
						cam = x[2] 
				return cam
		   	except:
				return None
		else:
			return None
			
		if serlist is not None:
			try:
				cardserver = ""
				for current in serlist.readlines():
					cardserver = current
				serlist.close()
			except:
				pass
		else:
			cardserver = " "

		if camdlist is not None:
			try:
				emu = ""
				for current in camdlist.readlines():
					emu = current
				camdlist.close()
			except:
				pass
		else:
			emu = " "
			
		return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
		
	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)

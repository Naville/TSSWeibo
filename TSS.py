# coding: UTF-8
import urllib2
import Weibo48
import json
import time
import sys
import weibo
WaitTime=40
class TSS:
	Weibo=Weibo48.Weibo48()
	SavedDict=dict()
	WebTSSdict=dict()
	DeletedDict=dict()
	def Save(self):
		f=open('TSS.txt','w')
		DictForWrite=dict()
		DictForWrite.update(self.WebTSSdict)
		DictForWrite.update(self.DeletedDict)
		string=json.dumps(DictForWrite)
		f.write(string)
		f.close()
   	def __init__(self):
   		f=open('TSS.txt','r')
   		try:
   			self.SavedDict=json.loads(f.read())
   		except ValueError:
   			self.SavedDict=dict()
   		f.close()
        
	def Post(self):
		for x in self.WebTSSdict.keys():
			statuesString=str(x)
			curDict=self.WebTSSdict[x]
			statuesString+=u'目前签署的版本有'
			for x in curDict['firmwares']:
				if(x['signing']==True):
					statuesString+=x['version']+u'开始于'+x['started']+","
			statuesString+='Powered By Twitter @__PAGEZERO @iNeal'
			DictWeibo={'Status':statuesString}
			try:
				self.Weibo.PostToWeibo(DictWeibo)
			except weibo.APIError as e:
				timeForS=self.APILimit()['RestSec']
				print "Reached API Limit,Have To Sleep For: "+str(timeForS)+"sec "
				time.sleep(timeForS)
				self.Weibo.PostToWeibo(DictWeibo)
			time.sleep(5)
		self.Save()
			
	def LoadFromWeb(self):
		response = urllib2.urlopen('http://api.ineal.me/tss/all')
		TSSdict = json.loads(response.read())
		print "Loaded From Web With"+str(len(TSSdict.keys()))+"Entries"
		for x in TSSdict.keys():
			if(self.SavedDict.has_key(x)):
				if(TSSdict[x]==self.SavedDict[x]):
					self.DeletedDict[x]=TSSdict[x]
					print x,'Didn\'t Change,Skip'
					del TSSdict[x]
		self.WebTSSdict=TSSdict

	def APILimit(self):

		return self.Weibo.APILimit()

a=TSS()
a.LoadFromWeb()
a.Post()
while True:
	print 'Sleep For 20min'
	time.sleep(20*60)#20Min*60Secw
	a=TSS()
	a.LoadFromWeb()
	a.Post()




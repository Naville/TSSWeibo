
from weibo import APIClient
import webbrowser
import os
import subprocess
import json
APP_KEY = '1999547747' # app key
APP_SECRET = '0bdb539e0d38ced514d207bf23e081e4' # app secret
CALLBACK_URL = 'http://navillezhang.me/WBCallBack.php' # callback url
class Weibo48:
	client=APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	#client=APIClient(app_key=APP_KEY, app_secret=APP_SECRET)
	Token=""
	def __init__(self):
		print "Init Weibo Object"
		url = self.client.get_authorize_url()
		print "Open This URL\n"
		print url+'\n'
		print "Token:\n"
		Token=raw_input()
		r = self.client.request_access_token(Token)
		access_token = r.access_token
		expires_in = r.expires_in #
		self.Token=access_token
		self.client.set_access_token(access_token, expires_in)
	def UploadMedia(self,Path,Type):
		strCommand='curl -H \"Authorization:OAuth2 '+self.Token+"\" -F \"media=@"+Path+"\" http://upload.api.weibo.com/2/mss/media_upload.json?type="+Type
		proc = subprocess.Popen([strCommand], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		#print out
		URL="http://upload.api.weibo.com/2/mss/media_msget.json?source="+APP_KEY+"&media_id="+json.loads(out)["media_id"]
		PID=self.client.statuses.upload_pic.post(pic=URL)["pic_id"]
		return PID
	def APILimit(self):
		data=self.client.account.rate_limit_status.get()
		returnVal=dict()
		returnVal['RestSec']=data['reset_time_in_seconds']
		returnVal['UserLimit']=data['user_limit']
		return returnVal
	def PostToWeibo(self,Dict):
		if(Dict.has_key('Photos')==False):
			Dict["Photos"]=list()
		if(Dict.has_key('Videos')==False):
			Dict["Videos"]=list()
		PhotoList=Dict["Photos"]
		VideoList=Dict["Videos"]
		StatusString=Dict["Status"]
		if(len(PhotoList)==0 and len(VideoList)==0):
			self.client.statuses.update.post(status=StatusString,lat="35.700988",long="139.771830")
			print "Weibo Posted"
		else:

			MediaIDList=[]
			for x in PhotoList:
				PID=self.UploadMedia(x,"image")
				os.remove(x)
				MediaIDList.append(PID)
			for y in VideoList:
				PID=self.UploadMedia(y,"video")

				MediaIDList.append(PID)
			print "MediaIDList:",MediaIDList
			PicIDString = ','.join(MediaIDList)
			print "PicIDString:",PicIDString
			self.client.statuses.upload_url_text.post(status=StatusString,pic_id=PicIDString,lat="35.700988",long="139.771830")
			print "Weibo Posted"

import subprocess
import string
from mailchimp3 import MailChimp
import pprint
import json
import time

YOUR_API_KEY = '<YOUR MAILCHIMP API KEY>'
YOUR_USERNAME = '<YOUR MAILCHIMP USERNAME>'

#create mailchimp client
client = MailChimp(mc_user=YOUR_USERNAME,mc_api=YOUR_API_KEY)

#valid MAC address to be filled in:
validMACs = ['<VAILD MAC ADDRESS OF DEVICE 1>','<VAILD MAC ADDRESS OF DEVICE 2>','<VAILD MAC ADDRESS OF DEVICE 3>',.....]

invalidMACs = {}

while 1:
	out = subprocess.check_output(['sudo','nmap','-sP','192.168.0.0/24'])#4th parameter is your network address change accordingly
	rawMAC=str(out).split('MAC Address: ')
	flag=0
	MAC=[]

	for elem in rawMAC:
        	if flag==0:
                	flag=1
                	continue
        	else:
                	MAC.append(elem.split()[0])

	print("MACS detected:\n")
	print(MAC)
	temp = []
	for i in invalidMACs:
		if i in MAC:
			continue
		else:
			temp.append(i)

	for i in temp:
		invalidMACs.pop(i, None)

	for i in MAC:
		if i in validMACs:
			continue
		else:
			if i in invalidMACs:
				continue
			else:
				invalidMACs[i]="1"



	print("Invalid MACs detected:\n")
	print(invalidMACs)
	flag=0

	for i in invalidMACs:
		if invalidMACs[i] == '1':
			flag=1

	if flag == 1:
		print("\nPreparing to send Mail:\n")
		#Create Campaign
		data={
			"type":"regular",
			"recipients":{
				"list_id":"<MAIL CHIMP LIST ID>"
				},
			"subject_line":"<SUBJECT OF EMAIL TO BE SENT>",
			"reply_to":"<YOUR MAIL ADDRESS TO REPLYTO>",
			"from_name":"<YOUR NAME/YOUR ORGNISATIONS NAME>",
			"settings":{"subject_line":"<SUBJECT OF EMAIL>","reply_to":"<YOUR MAIL ADDRESS>","from_name":"<YOUR NAME/YOUR ORGANISATION'S NAME>"}
				}
		pprint.pprint(client.campaigns.create(data))
		info = client.campaigns.create(data);


		html="<p>"
		for i in invalidMACs:
			if invalidMACs[i] == '1':
				html+="This invalid MAC "+i+" connected to your network <br>"
				invalidMACs[i] = '0'
		html+="</p>"
		pprint.pprint(client.campaigns.content.update(campaign_id=info['id'], data={"html": html}))
		pprint.pprint(client.campaigns.actions.send(campaign_id=info['id']))

	#Time interval to scan the network
	time.sleep(<ENTER FREQUENCY WITH WHICH THE NETWORK IS SCANNED IN SECONDS>)

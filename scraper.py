import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import subprocess
from pathlib import Path

URL = "https://eu01.playuntrusted.com/opsec/6899c8867e168932f2bbf70176b8b0c454743f70/"
headers = {
    'User-Agent': 'Ping-Untrusted-Scraper v.1.00',
    'From': 'sec@badping.live'  
}
r = requests.get(URL, headers=headers)
   
soup = BeautifulSoup(r.content, 'html5lib')

dir = soup.find('h1', attrs = {'style':'vertical-align: middle;text-align:center;'}) 
for row in dir:
    temp1_1 = row.replace('OPSEC #', "")
    path = Path(temp1_1)
    if os.path.isdir(path):
        print('Directory already exists!') 
        quit()
    else:
        path.mkdir(parents=True)
    
# Gets the information about the players from the OPSEC Operatives List
userinfo=[]

user_info = soup.find('div', attrs = {'style':'margin:auto;margin-bottom:-30px;'}) 

for row in user_info.findAll('td'):
    user1 = {}
    user1['username'] = row.a.text
    user1['user_url'] = row.a['href']
    user1['img'] = "https://eu01.playuntrusted.com"+row.img['src']
    temp1_1 = row.find_all("div",{"style":"font-size:1.0em;margin-top:3px;"})[0]
    temp1_2 = temp1_1.text
    temp1_3 = temp1_2.replace("as", "")
    temp1_4 = temp1_3.replace(" ", "")
    user1['color'] = temp1_4.replace('"', "")
    temp2_1 = row.find_all("div",{"style":"font-size:1.0em;margin-top:3px;"})[1]
    temp2_2 = temp2_1.text
    user1['equippable'] = temp2_2
    userinfo.append(user1)

filename = 'users.csv'
fpath = (path / filename).with_suffix('.csv')
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['username','user_url','img','color','equippable'])
    w.writeheader()
    for user1 in userinfo:
        w.writerow(user1)
        
# Gets the prechat from the game.
prechat=[]

prechat_info = soup.find('div', attrs = {'id':'prechat'}) 

for row in prechat_info.findAll('tr'):
    prechat1 = {}
    temp1_1 = row.find("td",{"style":"width:20%;text-align:right;"})
    temp1_2 = temp1_1.text
    prechat1['username'] = temp1_2.replace(':', "")
    temp2_1 = row.find_all("td")[1]
    prechat1['message'] = temp2_1.text
    prechat.append(prechat1)

filename = 'prechat.csv'
fpath = (path / filename).with_suffix('.csv')
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['username','message'])
    w.writeheader()
    for prechat1 in prechat:
        w.writerow(prechat1)
        
# Gets the operatives summary. I couldnt manage to get op logs, but I'm sure ill find a solution in the future
opsummary=[]

op_summary = soup.find_all('div',{"style":"margin:auto;"})[5]

for row in op_summary.findAll('tr'):
    opsummary1 = {}
    opsummary1['color'] = row.a.text
    temp1_1 = row.text
    temp1_2 = temp1_1.split()
    temp1_3 = temp1_2[5]+" "+temp1_2[6]
    opsummary1['started_as'] = temp1_3.replace(' and', "")
    temp2_1 = row.text
    temp2_2 = temp2_1.split()
    temp2_3 = temp2_2[9]+" "+temp2_2[10]+" "+temp2_2[11]
    temp2_4 = temp2_3.replace('as ', "")
    temp2_5 = temp2_4.replace('Obtained', "")
    temp2_6 = temp2_5.replace('.', "")
    temp2_7 = temp2_6.replace('  ', "")
    opsummary1['finished_as'] = re.sub(r'[0-9]+', '', temp2_7)
    temp3_1 = row.text
    temp3_2 = temp3_1.split()
    temp3_3 = temp3_2[-2]+" "+temp3_2[-1]
    temp3_4 = temp3_3.replace('credits', "")
    temp3_5 = temp3_4.replace(' ', "")
    temp3_6 = temp3_5.replace('.', "")
    opsummary1['heartbeat'] = temp3_6.replace('WINNER!', "")
    opsummary.append(opsummary1)

filename = 'opsummary.csv'
fpath = (path / filename).with_suffix('.csv')
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['color','started_as', 'finished_as','heartbeat'])
    w.writeheader()
    for opsummary1 in opsummary:
        w.writerow(opsummary1)
        
# Gets the messages from the game.
messages=[]

message_log = soup.find_all('tbody')[9]

        
for row in message_log.findAll('tr', recursive=False):
    messages1 = {}
    broadcast = 'ANONYMOUS BROADCAST:'
    mail = 'Private message:'
    messages1['messages'] = row
    temp1_1 = row.find('b')
    if messages1['messages'].find('td',{"style":"color:#ff0001;text-align:center;font-size:1.0em;"}):
        messages1['vote'] = "1"
    else:
        messages1['vote'] = ""
    if temp1_1 != None and broadcast in temp1_1:
        messages1['broadcast'] = "1"
    else:
        messages1['broadcast'] = ""
    if temp1_1 != None and mail in temp1_1:
        messages1['mail'] = "1"
    else:
        messages1['mail'] = ""
    for row2 in row.find_all('td',{"style":"text-align:left;width:25%;"}):
        if  messages1['messages'].find('td',{"style":"text-align:justify;width:75%;color: #ffc91b;;"}):
            messages1['asc'] = "1"
        else:
            messages1['asc'] = ""
        
        if  messages1['messages'].find('td',{"style":"text-align:justify;width:75%;color: #911eb4;;"}):
            messages1['dead'] = "1"
        else:
            messages1['dead'] = ""
        if  messages1['messages'].find('td',{"style":"text-align:justify;width:75%;color: #fff;;"}):
            messages1['alive'] = "1"
        else:
            messages1['alive'] = ""
    messages.append(messages1) 

filename = 'messages_temp.csv'
fpath = (path / filename).with_suffix('.csv')
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages'])
    w.writeheader()
    for messages1 in messages:
        w.writerow(messages1)
        
# Gets the topology from the game.
topology=[]

topology1 = {}
topology1['code'] = soup.find_all('div',{"style":"margin:auto;"})[2]
topology.append(topology1)

filename = 'topology.csv'
fpath = (path / filename).with_suffix('.csv')
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['code'])
    w.writeheader()
    for topology1 in topology:
        w.writerow(topology1)
        
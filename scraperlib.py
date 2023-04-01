def old(URL):# This is old code, for old logs
    import requests
    from bs4 import BeautifulSoup
    import csv
    import re
    import os
    from pathlib import Path

    headers = {
        'User-Agent': 'Ping-Untrusted-Scraper v.1.50',
        'From': 'Ping#6175'  
    }
    r = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    dir = soup.find('h1', attrs = {'style':'vertical-align: middle;text-align:center;'}) 
    for row in dir:
        global opsecid
        opsecid = row.replace('OPSEC #', "")
        path = Path(opsecid)
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
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
    with fpath.open(mode='w', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages','daychange'])
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['code'])
        w.writeheader()
        for topology1 in topology:
            w.writerow(topology1)
    
    # Messages 2 part of the csv.
    headers = {
        'User-Agent': 'Ping-Untrusted-Scraper v.1.50',
        'From': 'Ping#6175'  
    }
    r = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    dir = soup.find('h1', attrs = {'style':'vertical-align: middle;text-align:center;'}) 
    for row in dir:
        temp1_1 = row.replace('OPSEC #', "")
        path = Path(temp1_1)

    test = []

    temp_value = '0'
    temp1_value = '0'
    temp2_value = '0'
    private_log = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Private Event Logs «</td></tr>'
    fpath = (path / 'messages_temp').with_suffix('.csv')
    with fpath.open(mode='r', newline='',encoding="UTF-8") as csv_file:

        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            test1 = {}
            # Start of Day 0 Night 1 'day' entries
            if temp_value == "01":
                test1['day'] = '01'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>':
                temp_value = '01'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Preparation Night<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 0 Night 1
            # Start of Day 1 Night 0
            if temp_value == "10":
                test1['day'] = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>':
                temp_value = '10'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp_value == "11":
                test1['day'] = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>':
                temp_value = '11'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp_value == "20":
                test1['day'] = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>':
                temp_value = '20'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp_value == "21":
                test1['day'] = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>':
                temp_value = '21'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp_value == "30":
                test1['day'] = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>':
                temp_value = '30'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp_value == "31":
                test1['day'] = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>':
                temp_value = '31'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp_value == "40":
                test1['day'] = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>':
                temp_value = '40'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp_value == "41":
                test1['day'] = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>':
                temp_value = '41'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp_value == "50":
                test1['day'] = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>':
                temp_value = '50'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp_value == "51":
                test1['day'] = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>':
                temp_value = '51'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp_value == "60":
                test1['day'] = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>':
                temp_value = '60'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp_value == "61":
                test1['day'] = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>':
                temp_value = '61'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp_value == "70":
                test1['day'] = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>':
                temp_value = '70'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 7 Night 0
            # Start of Day 1 Night 1
            if temp_value == "71":
                test1['day'] = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>':
                temp_value = '71'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 7 Night 1
            # Start of Day 2 Night 0
            if temp_value == "80":
                test1['day'] = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>':
                temp_value = '80'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp_value == "81":
                test1['day'] = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>':
                temp_value = '81'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp_value == "90":
                test1['day'] = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>':
                temp_value = '90'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp_value == "91":
                test1['day'] = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>':
                temp_value = '91'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp_value == "100":
                test1['day'] = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>':
                temp_value = '100'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp_value == "101":
                test1['day'] = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>':
                temp_value = '101'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp_value == "110":
                test1['day'] = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 11 Chat Log «</td></tr>':
                temp_value = '110'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp_value == "111":
                test1['day'] = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 11 Chat Log «</td></tr>':
                temp_value = '111'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp_value == "120":
                test1['day'] = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 12 Chat Log «</td></tr>':
                temp_value = '120'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp_value == "121":
                test1['day'] = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 12 Chat Log «</td></tr>':
                temp_value = '121'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 12 Night 1 'day' entries
            # Start of Day 1 Night 0 'actions' entries
            if temp1_value == "10":
                test1['actions'] = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
                temp1_value = '10'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp1_value == "11":
                test1['actions'] = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
                temp1_value = '11'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp1_value == "20":
                test1['actions'] = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
                temp1_value = '20'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp1_value == "21":
                test1['actions'] = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
                temp1_value = '21'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp1_value == "30":
                test1['actions'] = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
                temp1_value = '30'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp1_value == "31":
                test1['actions'] = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
                temp1_value = '31'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp1_value == "40":
                test1['actions'] = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
                temp1_value = '40'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp1_value == "41":
                test1['actions'] = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
                temp1_value = '41'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp1_value == "50":
                test1['actions'] = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
                temp1_value = '50'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp1_value == "51":
                test1['actions'] = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
                temp1_value = '51'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp1_value == "60":
                test1['actions'] = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
                temp1_value = '60'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp1_value == "61":
                test1['actions'] = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
                temp1_value = '61'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp1_value == "70":
                test1['actions'] = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
                temp1_value = '70'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 7 Night 0
            # Start of Day 7 Night 1
            if temp1_value == "71":
                test1['actions'] = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
                temp1_value = '71'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 7 Night 1
            # Start of Day 8 Night 0
            if temp1_value == "80":
                test1['actions'] = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
                temp1_value = '80'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp1_value == "81":
                test1['actions'] = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
                temp1_value = '81'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp1_value == "90":
                test1['actions'] = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
                temp1_value = '90'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp1_value == "91":
                test1['actions'] = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
                temp1_value = '91'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp1_value == "100":
                test1['actions'] = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
                temp1_value = '100'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp1_value == "101":
                test1['actions'] = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
                temp1_value = '101'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp1_value == "110":
                test1['actions'] = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
                temp1_value = '110'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp1_value == "111":
                test1['actions'] = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
                temp1_value = '111'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp1_value == "120":
                test1['actions'] = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
                temp1_value = '120'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp1_value == "121":
                test1['actions'] = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
                temp1_value = '121'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 12 Night 1 'actions' entries
            # Start of Day 0 Night 0 'events' entries
            if temp2_value == "00":
                test1['events'] = '00'
            if line[9] == '<tr><td style="text-align:left;width:30%"></td><td style="text-align:left;width:70%"></td></tr>':
                temp2_value = '00'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Preparation Night<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 0 Night 0
            # Start of Day 1 Night 0 'events' entries
            if temp2_value == "10":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '10'
            if temp2_value == "1010": #skip the 'Public Event Log «'
                temp2_value = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
                temp2_value = '1010'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 1<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp2_value == "11":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '11'
            if temp2_value == "1111": #skip the 'Public Event Log «'
                temp2_value = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
                temp2_value = '1111'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 2<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp2_value == "20":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '20'
            if temp2_value == "2020": #skip the 'Public Event Log «'
                temp2_value = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
                temp2_value = '2020'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 2<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp2_value == "21":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '21'
            if temp2_value == "2121": #skip the 'Public Event Log «'
                temp2_value = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
                temp2_value = '2121'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 3<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp2_value == "30":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '30'
            if temp2_value == "3030": #skip the 'Public Event Log «'
                temp2_value = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
                temp2_value = '3030'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 3<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp2_value == "31":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '31'
            if temp2_value == "3131": #skip the 'Public Event Log «'
                temp2_value = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
                temp2_value = '3131'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 4<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp2_value == "40":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '40'
            if temp2_value == "4040": #skip the 'Public Event Log «'
                temp2_value = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
                temp2_value = '4040'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 4<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp2_value == "41":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '41'
            if temp2_value == "4141": #skip the 'Public Event Log «'
                temp2_value = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
                temp2_value = '4141'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 5<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp2_value == "50":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '50'
            if temp2_value == "5050": #skip the 'Public Event Log «'
                temp2_value = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
                temp2_value = '5050'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 5<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp2_value == "51":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '51'
            if temp2_value == "5151": #skip the 'Public Event Log «'
                temp2_value = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
                temp2_value = '5151'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp2_value == "60":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '60'
            if temp2_value == "6060": #skip the 'Public Event Log «'
                temp2_value = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
                temp2_value = '6060'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp2_value == "61":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '61'
            if temp2_value == "6161": #skip the 'Public Event Log «'
                temp2_value = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
                temp2_value = '6161'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 7<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp2_value == "70":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '70'
            if temp2_value == "7070": #skip the 'Public Event Log «'
                temp2_value = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
                temp2_value = '7070'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 7<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 7 Night 0
            # Start of Day 7 Night 1
            if temp2_value == "71":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '71'
            if temp2_value == "7171": #skip the 'Public Event Log «'
                temp2_value = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
                temp2_value = '7171'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 8<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 7 Night 1
            # Start of Day 8 Night 0
            if temp2_value == "80":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '80'
            if temp2_value == "8080": #skip the 'Public Event Log «'
                temp2_value = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
                temp2_value = '8080'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 8<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp2_value == "81":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '81'
            if temp2_value == "8181": #skip the 'Public Event Log «'
                temp2_value = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
                temp2_value = '8181'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 9<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp2_value == "90":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '90'
            if temp2_value == "9090": #skip the 'Public Event Log «'
                temp2_value = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
                temp2_value = '90'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 9<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp2_value == "91":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '91'
            if temp2_value == "9191": #skip the 'Public Event Log «'
                temp2_value = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
                temp2_value = '9191'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp2_value == "100":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '100'
            if temp2_value == "100100": #skip the 'Public Event Log «'
                temp2_value = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
                temp2_value = '100100'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 10<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp2_value == "101":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '101'
            if temp2_value == "101101": #skip the 'Public Event Log «'
                temp2_value = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
                temp2_value = '101101'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 11<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp2_value == "110":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '110'
            if temp2_value == "110110": #skip the 'Public Event Log «'
                temp2_value = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
                temp2_value = '110110'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 11<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp2_value == "111":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '111'
            if temp2_value == "111111": #skip the 'Public Event Log «'
                temp2_value = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
                temp2_value = '111111'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp2_value == "120":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '120'
            if temp2_value == "120120": #skip the 'Public Event Log «'
                temp2_value = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
                temp2_value = '120120'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp2_value == "121":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '121'
            if temp2_value == "121121": #skip the 'Public Event Log «'
                temp2_value = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
                temp2_value = '121121'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 12 Night 1 'events' 
            # Start of Day Change Findings
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>':
                    test1['daychange'] = '01'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>':
                    test1['daychange'] = 10
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>':
                    test1['daychange'] = 11
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>':
                    test1['daychange'] = 20
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>':
                    test1['daychange'] = 21
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>':
                    test1['daychange'] = 30
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>':
                    test1['daychange'] = 31
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>':
                    test1['daychange'] = 40
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>':
                    test1['daychange'] = 41
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>':
                    test1['daychange'] = 50
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>':
                    test1['daychange'] = 51
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>':
                    test1['daychange'] = 60
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>':
                    test1['daychange'] = 61
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>':
                    test1['daychange'] = 70
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>':
                    test1['daychange'] = 71
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>':
                    test1['daychange'] = 80
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>':
                    test1['daychange'] = 81
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>':
                    test1['daychange'] = 90
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>':
                    test1['daychange'] = 91
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>':
                    test1['daychange'] = 100
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>':
                    test1['daychange'] = 101
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 11 Chat Log «</td></tr>':
                    test1['daychange'] = 110
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 11 Chat Log «</td></tr>':
                    test1['daychange'] = 111
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 12 Chat Log «</td></tr>':
                    test1['daychange'] = 120
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 12 Chat Log «</td></tr>':
                    test1['daychange'] = 121
            # End of Day Change Findings
            test1['asc'] = line[3]
            test1['dead'] = line[4]
            test1['alive'] = line[5]
            test1['broadcast'] = line[6]
            test1['mail'] = line[7]
            test1['vote'] = line[8]
            test1['messages'] = line[9]
            test.append(test1)
            
    filename = 'messages.csv'
    fpath = (path / filename).with_suffix('.csv')
    with fpath.open(mode='w', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages','daychange'],quoting=csv.QUOTE_ALL)
        w.writeheader()
        for test1 in test:
            w.writerow(test1)
    
    # Done, now remove the temp files
    os.remove(Path(opsecid+'\\messages_temp.csv'))
    
    # Now generate php script
    genphp(opsecid)

def new(URL): # This is new code, for new logs
    import requests
    from bs4 import BeautifulSoup
    import csv
    import re
    import os
    from pathlib import Path

    headers = {
        'User-Agent': 'Ping-Untrusted-Scraper v.1.50',
        'From': 'Ping#6175'  
    }
    r = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    dir = soup.find('h1', attrs = {'style':'vertical-align: middle;text-align:center;'}) 
    for row in dir:
        opsecid = row.replace('OPSEC #', "")
        path = Path(opsecid)
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['color','started_as', 'finished_as','heartbeat'])
        w.writeheader()
        for opsummary1 in opsummary:
            w.writerow(opsummary1)
            
    # Gets the messages from the game.
    messages=[]

    message_log = soup.find_all('tbody')[5]
    
    #! This is why it works, and why the old doesnt
            
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
    with fpath.open(mode='w', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages','daychange'])
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
    with fpath.open(mode='w+', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['code'])
        w.writeheader()
        for topology1 in topology:
            w.writerow(topology1)
    
    # Messages 2 part of the csv.

    headers = {
        'User-Agent': 'Ping-Untrusted-Scraper v.1.50',
        'From': 'Ping#6175'  
    }
    r = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    dir = soup.find('h1', attrs = {'style':'vertical-align: middle;text-align:center;'}) 
    for row in dir:
        temp1_1 = row.replace('OPSEC #', "")
        path = Path(temp1_1)

    test = []

    temp_value = '0'
    temp1_value = '0'
    temp2_value = '0'
    private_log = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Private Event Logs «</td></tr>'
    fpath = (path / 'messages_temp').with_suffix('.csv')
    with fpath.open(mode='r', newline='',encoding="UTF-8") as csv_file:

        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            test1 = {}
            # Start of Day 0 Night 1 'day' entries
            if temp_value == "01":
                test1['day'] = '01'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>':
                temp_value = '01'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Preparation Night<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 0 Night 1
            # Start of Day 1 Night 0
            if temp_value == "10":
                test1['day'] = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>':
                temp_value = '10'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp_value == "11":
                test1['day'] = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>':
                temp_value = '11'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp_value == "20":
                test1['day'] = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>':
                temp_value = '20'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp_value == "21":
                test1['day'] = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>':
                temp_value = '21'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp_value == "30":
                test1['day'] = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>':
                temp_value = '30'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp_value == "31":
                test1['day'] = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>':
                temp_value = '31'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp_value == "40":
                test1['day'] = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>':
                temp_value = '40'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp_value == "41":
                test1['day'] = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>':
                temp_value = '41'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp_value == "50":
                test1['day'] = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>':
                temp_value = '50'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp_value == "51":
                test1['day'] = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>':
                temp_value = '51'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp_value == "60":
                test1['day'] = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>':
                temp_value = '60'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp_value == "61":
                test1['day'] = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>':
                temp_value = '61'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp_value == "70":
                test1['day'] = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>':
                temp_value = '70'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 7 Night 0
            # Start of Day 1 Night 1
            if temp_value == "71":
                test1['day'] = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>':
                temp_value = '71'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 7 Night 1
            # Start of Day 2 Night 0
            if temp_value == "80":
                test1['day'] = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>':
                temp_value = '80'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp_value == "81":
                test1['day'] = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>':
                temp_value = '81'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp_value == "90":
                test1['day'] = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>':
                temp_value = '90'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp_value == "91":
                test1['day'] = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>':
                temp_value = '91'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp_value == "100":
                test1['day'] = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>':
                temp_value = '100'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp_value == "101":
                test1['day'] = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>':
                temp_value = '101'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp_value == "110":
                test1['day'] = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 11 Chat Log «</td></tr>':
                temp_value = '110'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp_value == "111":
                test1['day'] = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 11 Chat Log «</td></tr>':
                temp_value = '111'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp_value == "120":
                test1['day'] = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 12 Chat Log «</td></tr>':
                temp_value = '120'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp_value == "121":
                test1['day'] = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 12 Chat Log «</td></tr>':
                temp_value = '121'
                test1['day'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
                test1['day'] = ''
                temp_value = '0'
            if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
                test1['day'] = ''
                temp_value = '0'
            # End of Day 12 Night 1 'day' entries
            # Start of Day 1 Night 0 'actions' entries
            if temp1_value == "10":
                test1['actions'] = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
                temp1_value = '10'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp1_value == "11":
                test1['actions'] = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
                temp1_value = '11'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp1_value == "20":
                test1['actions'] = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
                temp1_value = '20'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp1_value == "21":
                test1['actions'] = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
                temp1_value = '21'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp1_value == "30":
                test1['actions'] = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
                temp1_value = '30'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp1_value == "31":
                test1['actions'] = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
                temp1_value = '31'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp1_value == "40":
                test1['actions'] = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
                temp1_value = '40'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp1_value == "41":
                test1['actions'] = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
                temp1_value = '41'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp1_value == "50":
                test1['actions'] = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
                temp1_value = '50'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp1_value == "51":
                test1['actions'] = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
                temp1_value = '51'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp1_value == "60":
                test1['actions'] = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
                temp1_value = '60'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp1_value == "61":
                test1['actions'] = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
                temp1_value = '61'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp1_value == "70":
                test1['actions'] = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
                temp1_value = '70'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 7 Night 0
            # Start of Day 7 Night 1
            if temp1_value == "71":
                test1['actions'] = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
                temp1_value = '71'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 7 Night 1
            # Start of Day 8 Night 0
            if temp1_value == "80":
                test1['actions'] = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
                temp1_value = '80'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp1_value == "81":
                test1['actions'] = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
                temp1_value = '81'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp1_value == "90":
                test1['actions'] = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
                temp1_value = '90'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp1_value == "91":
                test1['actions'] = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
                temp1_value = '91'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp1_value == "100":
                test1['actions'] = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
                temp1_value = '100'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp1_value == "101":
                test1['actions'] = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
                temp1_value = '101'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp1_value == "110":
                test1['actions'] = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
                temp1_value = '110'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp1_value == "111":
                test1['actions'] = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
                temp1_value = '111'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp1_value == "120":
                test1['actions'] = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
                temp1_value = '120'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp1_value == "121":
                test1['actions'] = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
                temp1_value = '121'
                test1['actions'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
                test1['actions'] = ''
                temp1_value = '0'
            # End of Day 12 Night 1 'actions' entries
            # Start of Day 0 Night 0 'events' entries
            if temp2_value == "00":
                test1['events'] = '00'
            if line[9] == '<tr><td style="text-align:left;width:30%"></td><td style="text-align:left;width:70%"></td></tr>':
                temp2_value = '00'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Preparation Night<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 0 Night 0
            # Start of Day 1 Night 0 'events' entries
            if temp2_value == "10":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '10'
            if temp2_value == "1010": #skip the 'Public Event Log «'
                temp2_value = '10'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
                temp2_value = '1010'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 1<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 1 Night 0
            # Start of Day 1 Night 1
            if temp2_value == "11":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '11'
            if temp2_value == "1111": #skip the 'Public Event Log «'
                temp2_value = '11'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
                temp2_value = '1111'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 2<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 1 Night 1
            # Start of Day 2 Night 0
            if temp2_value == "20":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '20'
            if temp2_value == "2020": #skip the 'Public Event Log «'
                temp2_value = '20'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
                temp2_value = '2020'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 2<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 2 Night 0
            # Start of Day 2 Night 1
            if temp2_value == "21":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '21'
            if temp2_value == "2121": #skip the 'Public Event Log «'
                temp2_value = '21'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
                temp2_value = '2121'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 3<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 2 Night 1
            # Start of Day 3 Night 0
            if temp2_value == "30":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '30'
            if temp2_value == "3030": #skip the 'Public Event Log «'
                temp2_value = '30'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
                temp2_value = '3030'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 3<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 3 Night 0
            # Start of Day 3 Night 1
            if temp2_value == "31":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '31'
            if temp2_value == "3131": #skip the 'Public Event Log «'
                temp2_value = '31'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
                temp2_value = '3131'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 4<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 3 Night 1
            # Start of Day 4 Night 0
            if temp2_value == "40":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '40'
            if temp2_value == "4040": #skip the 'Public Event Log «'
                temp2_value = '40'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
                temp2_value = '4040'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 4<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 4 Night 0
            # Start of Day 4 Night 1
            if temp2_value == "41":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '41'
            if temp2_value == "4141": #skip the 'Public Event Log «'
                temp2_value = '41'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
                temp2_value = '4141'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 5<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 4 Night 1
            # Start of Day 5 Night 0
            if temp2_value == "50":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '50'
            if temp2_value == "5050": #skip the 'Public Event Log «'
                temp2_value = '50'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
                temp2_value = '5050'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 5<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 5 Night 0
            # Start of Day 5 Night 1
            if temp2_value == "51":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '51'
            if temp2_value == "5151": #skip the 'Public Event Log «'
                temp2_value = '51'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
                temp2_value = '5151'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 5 Night 1
            # Start of Day 6 Night 0
            if temp2_value == "60":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '60'
            if temp2_value == "6060": #skip the 'Public Event Log «'
                temp2_value = '60'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
                temp2_value = '6060'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 6 Night 0
            # Start of Day 6 Night 1
            if temp2_value == "61":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '61'
            if temp2_value == "6161": #skip the 'Public Event Log «'
                temp2_value = '61'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
                temp2_value = '6161'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 7<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 6 Night 1
            # Start of Day 7 Night 0
            if temp2_value == "70":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '70'
            if temp2_value == "7070": #skip the 'Public Event Log «'
                temp2_value = '70'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
                temp2_value = '7070'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 7<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 7 Night 0
            # Start of Day 7 Night 1
            if temp2_value == "71":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '71'
            if temp2_value == "7171": #skip the 'Public Event Log «'
                temp2_value = '71'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
                temp2_value = '7171'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 8<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 7 Night 1
            # Start of Day 8 Night 0
            if temp2_value == "80":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '80'
            if temp2_value == "8080": #skip the 'Public Event Log «'
                temp2_value = '80'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
                temp2_value = '8080'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 8<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 8 Night 0
            # Start of Day 8 Night 1
            if temp2_value == "81":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '81'
            if temp2_value == "8181": #skip the 'Public Event Log «'
                temp2_value = '81'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
                temp2_value = '8181'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 9<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 8 Night 1
            # Start of Day 9 Night 0
            if temp2_value == "90":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '90'
            if temp2_value == "9090": #skip the 'Public Event Log «'
                temp2_value = '90'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
                temp2_value = '90'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 9<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 9 Night 0
            # Start of Day 9 Night 1
            if temp2_value == "91":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '91'
            if temp2_value == "9191": #skip the 'Public Event Log «'
                temp2_value = '91'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
                temp2_value = '9191'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 9 Night 1
            # Start of Day 10 Night 0
            if temp2_value == "100":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '100'
            if temp2_value == "100100": #skip the 'Public Event Log «'
                temp2_value = '100'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
                temp2_value = '100100'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 10<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 10 Night 0
            # Start of Day 10 Night 1
            if temp2_value == "101":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '101'
            if temp2_value == "101101": #skip the 'Public Event Log «'
                temp2_value = '101'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
                temp2_value = '101101'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 11<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 10 Night 1
            # Start of Day 11 Night 0
            if temp2_value == "110":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '110'
            if temp2_value == "110110": #skip the 'Public Event Log «'
                temp2_value = '110'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
                temp2_value = '110110'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 11<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 11 Night 0
            # Start of Day 11 Night 1
            if temp2_value == "111":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '111'
            if temp2_value == "111111": #skip the 'Public Event Log «'
                temp2_value = '111'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
                temp2_value = '111111'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 11 Night 1
            # Start of Day 12 Night 0
            if temp2_value == "120":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '120'
            if temp2_value == "120120": #skip the 'Public Event Log «'
                temp2_value = '120'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
                temp2_value = '120120'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 12 Night 0
            # Start of Day 12 Night 1
            if temp2_value == "121":
                if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                    test1['events'] = ''
                else:
                    test1['events'] = '121'
            if temp2_value == "121121": #skip the 'Public Event Log «'
                temp2_value = '121'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
                temp2_value = '121121'
                test1['events'] = ''
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
                test1['events'] = ''
                temp2_value = '0'
            # End of Day 12 Night 1 'events' 
            # Start of Day Change Findings
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>':
                    test1['daychange'] = '01'
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>':
                    test1['daychange'] = 10
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>':
                    test1['daychange'] = 11
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>':
                    test1['daychange'] = 20
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>':
                    test1['daychange'] = 21
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>':
                    test1['daychange'] = 30
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>':
                    test1['daychange'] = 31
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>':
                    test1['daychange'] = 40
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>':
                    test1['daychange'] = 41
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>':
                    test1['daychange'] = 50
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>':
                    test1['daychange'] = 51
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>':
                    test1['daychange'] = 60
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>':
                    test1['daychange'] = 61
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>':
                    test1['daychange'] = 70
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>':
                    test1['daychange'] = 71
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>':
                    test1['daychange'] = 80
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>':
                    test1['daychange'] = 81
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>':
                    test1['daychange'] = 90
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>':
                    test1['daychange'] = 91
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>':
                    test1['daychange'] = 100
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>':
                    test1['daychange'] = 101
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 11 Chat Log «</td></tr>':
                    test1['daychange'] = 110
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 11 Chat Log «</td></tr>':
                    test1['daychange'] = 111
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 12 Chat Log «</td></tr>':
                    test1['daychange'] = 120
            if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 12 Chat Log «</td></tr>':
                    test1['daychange'] = 121
            # End of Day Change Findings
            test1['asc'] = line[3]
            test1['dead'] = line[4]
            test1['alive'] = line[5]
            test1['broadcast'] = line[6]
            test1['mail'] = line[7]
            test1['vote'] = line[8]
            test1['messages'] = line[9]
            test.append(test1)
            
    filename = 'messages.csv'
    fpath = (path / filename).with_suffix('.csv')
    with fpath.open(mode='w', newline='',encoding="UTF-8") as f:
        w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages','daychange'],quoting=csv.QUOTE_ALL)
        w.writeheader()
        for test1 in test:
            w.writerow(test1)
            
    # Done, now remove the temp files
    os.remove(Path(opsecid+'\\messages_temp.csv'))
    
    # Now generate php script
    genphp(opsecid)

def auto(URL):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        'User-Agent': 'Ping-Untrusted-Scraper v.1.50',
        'From': 'Ping#6175'  
    }
    r = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib')
    
    finder = soup.find_all('tbody')[9] # Checks for the old()
    
    if 'Preparation Night Chat Log' in str(finder):
        # Run old()
        old(URL)
    else:
        # We would eventually check every possibilitym but for now we'll just run new()
        new(URL)
        
def genphp(OpsecNum):
    import configparser
    from pathlib import Path
    
    config = configparser.ConfigParser()
    config.read('settings.ini')
    if config['SETTINGS']['use_php'] == '1':
        with open('template.php', 'r') as file :
            filedata = file.read()
             
        filename = Path(OpsecNum+'\\'+OpsecNum+'.php')
        
        with open(filename, 'w') as file:
            file.write(filedata)
    
#   import logging
#   logging.basicConfig(filename='output.txt', level=logging.DEBUG, format='')
#   logging.debug(finder)
# Just some debugging code for future use.
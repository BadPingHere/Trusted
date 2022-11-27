import requests
from bs4 import BeautifulSoup
import csv
import re
import os
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

test = []

temp_value = '0'
temp1_value = '0'
temp2_value = '0'
private_log = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Private Event Logs «</td></tr>'
fpath = (path / 'messages_temp').with_suffix('.csv')
with fpath.open(mode='r', newline='') as csv_file:

    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        test1 = {}
        # Start of Day 0 Night 1 'day' entries
        if temp_value == "0_1":
            test1['day'] = '0_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>':
            temp_value = '0_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Preparation Night<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 0 Night 1
        # Start of Day 1 Night 0
        if temp_value == "1_0":
            test1['day'] = '1_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>':
            temp_value = '1_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 1 Night 0
        # Start of Day 1 Night 1
        if temp_value == "1_1":
            test1['day'] = '1_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>':
            temp_value = '1_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 1 Night 1
        # Start of Day 2 Night 0
        if temp_value == "2_0":
            test1['day'] = '2_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>':
            temp_value = '2_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 2 Night 0
        # Start of Day 2 Night 1
        if temp_value == "2_1":
            test1['day'] = '2_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>':
            temp_value = '2_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 2 Night 1
        # Start of Day 3 Night 0
        if temp_value == "3_0":
            test1['day'] = '3_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>':
            temp_value = '3_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 3 Night 0
        # Start of Day 3 Night 1
        if temp_value == "3_1":
            test1['day'] = '3_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>':
            temp_value = '3_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 3 Night 1
        # Start of Day 4 Night 0
        if temp_value == "4_0":
            test1['day'] = '4_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>':
            temp_value = '4_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 4 Night 0
        # Start of Day 4 Night 1
        if temp_value == "4_1":
            test1['day'] = '4_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>':
            temp_value = '4_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 4 Night 1
        # Start of Day 5 Night 0
        if temp_value == "5_0":
            test1['day'] = '5_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>':
            temp_value = '5_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 5 Night 0
        # Start of Day 5 Night 1
        if temp_value == "5_1":
            test1['day'] = '5_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>':
            temp_value = '5_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 5 Night 1
        # Start of Day 6 Night 0
        if temp_value == "6_0":
            test1['day'] = '6_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>':
            temp_value = '6_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 6 Night 0
        # Start of Day 6 Night 1
        if temp_value == "6_1":
            test1['day'] = '6_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>':
            temp_value = '6_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 6 Night 1
        # Start of Day 7 Night 0
        if temp_value == "7_0":
            test1['day'] = '7_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>':
            temp_value = '7_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 7 Night 0
        # Start of Day 1 Night 1
        if temp_value == "7_1":
            test1['day'] = '7_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>':
            temp_value = '7_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 7 Night 1
        # Start of Day 2 Night 0
        if temp_value == "8_0":
            test1['day'] = '8_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>':
            temp_value = '8_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 8 Night 0
        # Start of Day 8 Night 1
        if temp_value == "8_1":
            test1['day'] = '8_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>':
            temp_value = '8_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 8 Night 1
        # Start of Day 9 Night 0
        if temp_value == "9_0":
            test1['day'] = '9_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>':
            temp_value = '9_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 9 Night 0
        # Start of Day 9 Night 1
        if temp_value == "9_1":
            test1['day'] = '9_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>':
            temp_value = '9_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 9 Night 1
        # Start of Day 10 Night 0
        if temp_value == "10_1":
            test1['day'] = '10_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>':
            temp_value = '10_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 10 Night 0
        # Start of Day 10 Night 1
        if temp_value == "10_1":
            test1['day'] = '10_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>':
            temp_value = '10_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 10 Night 1
        # Start of Day 11 Night 0
        if temp_value == "11_0":
            test1['day'] = '11_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 11 Chat Log «</td></tr>':
            temp_value = '11_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 11 Night 0
        # Start of Day 11 Night 1
        if temp_value == "11_1":
            test1['day'] = '11_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 11 Chat Log «</td></tr>':
            temp_value = '11_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 11 Night 1
        # Start of Day 12 Night 0
        if temp_value == "12_0":
            test1['day'] = '12_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 12 Chat Log «</td></tr>':
            temp_value = '12_0'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 12 Night 0
        # Start of Day 12 Night 1
        if temp_value == "12_1":
            test1['day'] = '12_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 12 Chat Log «</td></tr>':
            temp_value = '12_1'
            test1['day'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
            test1['day'] = ''
            temp_value = '0'
        if line[9] == '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>':
            test1['day'] = ''
            temp_value = '0'
        # End of Day 12 Night 1 'day' entries
        # Start of Day 1 Night 0 'actions' entries
        if temp1_value == "1_0":
            test1['actions'] = '1_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 1<hr/></td></tr>':
            temp1_value = '1_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 1 Night 0
        # Start of Day 1 Night 1
        if temp1_value == "1_1":
            test1['actions'] = '1_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 1<hr/></td></tr>':
            temp1_value = '1_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 1 Night 1
        # Start of Day 2 Night 0
        if temp1_value == "2_0":
            test1['actions'] = '2_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 2<hr/></td></tr>':
            temp1_value = '2_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 2 Night 0
        # Start of Day 2 Night 1
        if temp1_value == "2_1":
            test1['actions'] = '2_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 2<hr/></td></tr>':
            temp1_value = '2_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 2 Night 1
        # Start of Day 3 Night 0
        if temp1_value == "3_0":
            test1['actions'] = '3_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 3<hr/></td></tr>':
            temp1_value = '3_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 3 Night 0
        # Start of Day 3 Night 1
        if temp1_value == "3_1":
            test1['actions'] = '3_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 3<hr/></td></tr>':
            temp1_value = '3_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 3 Night 1
        # Start of Day 4 Night 0
        if temp1_value == "4_0":
            test1['actions'] = '4_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 4<hr/></td></tr>':
            temp1_value = '4_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 4 Night 0
        # Start of Day 4 Night 1
        if temp1_value == "4_1":
            test1['actions'] = '4_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 4<hr/></td></tr>':
            temp1_value = '4_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 4 Night 1
        # Start of Day 5 Night 0
        if temp1_value == "5_0":
            test1['actions'] = '5_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 5<hr/></td></tr>':
            temp1_value = '5_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 5 Night 0
        # Start of Day 5 Night 1
        if temp1_value == "5_1":
            test1['actions'] = '5_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 5<hr/></td></tr>':
            temp1_value = '5_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 5 Night 1
        # Start of Day 6 Night 0
        if temp1_value == "6_0":
            test1['actions'] = '6_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 6<hr/></td></tr>':
            temp1_value = '6_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 6 Night 0
        # Start of Day 6 Night 1
        if temp1_value == "6_1":
            test1['actions'] = '6_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 6<hr/></td></tr>':
            temp1_value = '6_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 6 Night 1
        # Start of Day 7 Night 0
        if temp1_value == "7_0":
            test1['actions'] = '7_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 7<hr/></td></tr>':
            temp1_value = '7_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 7 Night 0
        # Start of Day 7 Night 1
        if temp1_value == "7_1":
            test1['actions'] = '7_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 7<hr/></td></tr>':
            temp1_value = '7_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 7 Night 1
        # Start of Day 8 Night 0
        if temp1_value == "8_0":
            test1['actions'] = '8_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 8<hr/></td></tr>':
            temp1_value = '8_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 8 Night 0
        # Start of Day 8 Night 1
        if temp1_value == "8_1":
            test1['actions'] = '8_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 8<hr/></td></tr>':
            temp1_value = '8_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 8 Night 1
        # Start of Day 9 Night 0
        if temp1_value == "9_0":
            test1['actions'] = '9_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 9<hr/></td></tr>':
            temp1_value = '9_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 9 Night 0
        # Start of Day 9 Night 1
        if temp1_value == "9_1":
            test1['actions'] = '9_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 9<hr/></td></tr>':
            temp1_value = '9_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 9 Night 1
        # Start of Day 6 Night 0
        if temp1_value == "10_0":
            test1['actions'] = '10_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 10<hr/></td></tr>':
            temp1_value = '10_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 10 Night 0
        # Start of Day 10 Night 1
        if temp1_value == "10_1":
            test1['actions'] = '10_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 10<hr/></td></tr>':
            temp1_value = '10_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 10 Night 1
        # Start of Day 11 Night 0
        if temp1_value == "11_0":
            test1['actions'] = '11_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 11<hr/></td></tr>':
            temp1_value = '11_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 11 Night 0
        # Start of Day 11 Night 1
        if temp1_value == "11_1":
            test1['actions'] = '11_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 11<hr/></td></tr>':
            temp1_value = '11_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 11 Night 1
        # Start of Day 12 Night 0
        if temp1_value == "12_0":
            test1['actions'] = '12_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Day 12<hr/></td></tr>':
            temp1_value = '12_0'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 12 Night 0
        # Start of Day 12 Night 1
        if temp1_value == "12_1":
            test1['actions'] = '12_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Committed Actions On Night 12<hr/></td></tr>':
            temp1_value = '12_1'
            test1['actions'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
            test1['actions'] = ''
            temp1_value = '0'
        # End of Day 12 Night 1 'actions' entries
        # Start of Day 0 Night 0 'events' entries
        if temp2_value == "0_0":
            test1['events'] = '0_0'
        if line[9] == '<tr><td style="text-align:left;width:30%"></td><td style="text-align:left;width:70%"></td></tr>':
            temp2_value = '0_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Preparation Night<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 0 Night 0
        # Start of Day 1 Night 0 'events' entries
        if temp2_value == "1_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '1_0'
        if temp2_value == "1_01_0": #skip the 'Public Event Log «'
            temp2_value = '1_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 1<hr/></td></tr>':
            temp2_value = '1_01_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 1<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 1 Night 0
        # Start of Day 1 Night 1
        if temp2_value == "1_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '1_1'
        if temp2_value == "1_11_1": #skip the 'Public Event Log «'
            temp2_value = '1_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 1<hr/></td></tr>':
            temp2_value = '1_11_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 2<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 1 Night 1
        # Start of Day 2 Night 0
        if temp2_value == "2_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '2_0'
        if temp2_value == "2_02_0": #skip the 'Public Event Log «'
            temp2_value = '2_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 2<hr/></td></tr>':
            temp2_value = '2_02_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 2<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 2 Night 0
        # Start of Day 2 Night 1
        if temp2_value == "2_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '2_1'
        if temp2_value == "2_12_1": #skip the 'Public Event Log «'
            temp2_value = '2_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 2<hr/></td></tr>':
            temp2_value = '2_12_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 3<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 2 Night 1
        # Start of Day 3 Night 0
        if temp2_value == "3_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '3_0'
        if temp2_value == "3_03_0": #skip the 'Public Event Log «'
            temp2_value = '3_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 3<hr/></td></tr>':
            temp2_value = '3_03_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 3<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 3 Night 0
        # Start of Day 3 Night 1
        if temp2_value == "3_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '3_1'
        if temp2_value == "3_13_1": #skip the 'Public Event Log «'
            temp2_value = '3_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 3<hr/></td></tr>':
            temp2_value = '3_13_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 4<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 3 Night 1
        # Start of Day 4 Night 0
        if temp2_value == "4_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '4_0'
        if temp2_value == "4_04_0": #skip the 'Public Event Log «'
            temp2_value = '4_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 4<hr/></td></tr>':
            temp2_value = '4_04_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 4<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 4 Night 0
        # Start of Day 4 Night 1
        if temp2_value == "4_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '4_1'
        if temp2_value == "4_14_1": #skip the 'Public Event Log «'
            temp2_value = '4_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 4<hr/></td></tr>':
            temp2_value = '4_14_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 5<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 4 Night 1
        # Start of Day 5 Night 0
        if temp2_value == "5_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '5_0'
        if temp2_value == "5_05_0": #skip the 'Public Event Log «'
            temp2_value = '5_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 5<hr/></td></tr>':
            temp2_value = '5_05_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 5<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 5 Night 0
        # Start of Day 5 Night 1
        if temp2_value == "5_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '5_1'
        if temp2_value == "5_15_1": #skip the 'Public Event Log «'
            temp2_value = '5_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 5<hr/></td></tr>':
            temp2_value = '5_15_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 5 Night 1
        # Start of Day 6 Night 0
        if temp2_value == "6_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '6_0'
        if temp2_value == "6_06_0": #skip the 'Public Event Log «'
            temp2_value = '6_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 6<hr/></td></tr>':
            temp2_value = '6_06_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 6<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 6 Night 0
        # Start of Day 6 Night 1
        if temp2_value == "6_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '6_1'
        if temp2_value == "6_16_1": #skip the 'Public Event Log «'
            temp2_value = '6_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 6<hr/></td></tr>':
            temp2_value = '6_16_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 7<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 6 Night 1
        # Start of Day 7 Night 0
        if temp2_value == "7_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '7_0'
        if temp2_value == "7_07_0": #skip the 'Public Event Log «'
            temp2_value = '7_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 7<hr/></td></tr>':
            temp2_value = '7_07_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 7<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 7 Night 0
        # Start of Day 7 Night 1
        if temp2_value == "7_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '7_1'
        if temp2_value == "7_17_1": #skip the 'Public Event Log «'
            temp2_value = '7_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 7<hr/></td></tr>':
            temp2_value = '7_17_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 8<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 7 Night 1
        # Start of Day 8 Night 0
        if temp2_value == "8_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '8_0'
        if temp2_value == "8_08_0": #skip the 'Public Event Log «'
            temp2_value = '8_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 8<hr/></td></tr>':
            temp2_value = '8_08_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 8<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 8 Night 0
        # Start of Day 8 Night 1
        if temp2_value == "8_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '8_1'
        if temp2_value == "8_18_1": #skip the 'Public Event Log «'
            temp2_value = '8_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 8<hr/></td></tr>':
            temp2_value = '8_18_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 9<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 8 Night 1
        # Start of Day 9 Night 0
        if temp2_value == "9_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '9_0'
        if temp2_value == "9_09_0": #skip the 'Public Event Log «'
            temp2_value = '9_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 9<hr/></td></tr>':
            temp2_value = '9_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 9<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 9 Night 0
        # Start of Day 9 Night 1
        if temp2_value == "9_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '9_1'
        if temp2_value == "9_19_1": #skip the 'Public Event Log «'
            temp2_value = '9_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 9<hr/></td></tr>':
            temp2_value = '9_19_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 6<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 9 Night 1
        # Start of Day 10 Night 0
        if temp2_value == "10_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '10_0'
        if temp2_value == "10_010_0": #skip the 'Public Event Log «'
            temp2_value = '10_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 10<hr/></td></tr>':
            temp2_value = '10_010_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 10<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 10 Night 0
        # Start of Day 10 Night 1
        if temp2_value == "10_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '10_1'
        if temp2_value == "10_110_1": #skip the 'Public Event Log «'
            temp2_value = '10_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 10<hr/></td></tr>':
            temp2_value = '10_110_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 11<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 10 Night 1
        # Start of Day 11 Night 0
        if temp2_value == "11_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '11_0'
        if temp2_value == "11_011_0": #skip the 'Public Event Log «'
            temp2_value = '11_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 11<hr/></td></tr>':
            temp2_value = '11_011_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 11<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 11 Night 0
        # Start of Day 11 Night 1
        if temp2_value == "11_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '11_1'
        if temp2_value == "11_111_1": #skip the 'Public Event Log «'
            temp2_value = '11_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 11<hr/></td></tr>':
            temp2_value = '7_17_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 11 Night 1
        # Start of Day 12 Night 0
        if temp2_value == "12_0":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '12_0'
        if temp2_value == "12_012_0": #skip the 'Public Event Log «'
            temp2_value = '12_0'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Day 12<hr/></td></tr>':
            temp2_value = '12_012_0'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Night 12<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 12 Night 0
        # Start of Day 12 Night 1
        if temp2_value == "12_1":
            if line[9] != None and private_log in line[9]: #checks for the 'Private Event Log «'
                test1['events'] = ''
            else:
                test1['events'] = '12_1'
        if temp2_value == "12_112_1": #skip the 'Public Event Log «'
            temp2_value = '12_1'
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/>Events for Night 12<hr/></td></tr>':
            temp2_value = '12_112_1'
            test1['events'] = ''
        if line[9] == '<tr><td colspan="2" style="color:#00ff01;text-align:center;font-size:1.5em;"> <hr/> Day 12<hr/></td></tr>':
            test1['events'] = ''
            temp2_value = '0'
        # End of Day 12 Night 1 'events' 
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
with fpath.open(mode='w+', newline='') as f:
    w = csv.DictWriter(f,['day','actions','events','asc','dead','alive','broadcast','mail','vote','messages'])
    w.writeheader()
    for test1 in test:
        w.writerow(test1)
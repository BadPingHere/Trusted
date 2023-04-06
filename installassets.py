import requests
from bs4 import BeautifulSoup
from pathlib import Path
from alive_progress import alive_bar

def installclasses():
    headers = {
        'User-Agent': 'Ping-Untrusted-Asset-Scraper v.1.10',
        'From': 'Ping#6175'  
    }
    URL = "https://www.playuntrusted.com/manual/classes/"
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html5lib')

    classes = soup.find_all('img', attrs = {'style':'width:128px;height:128px;float:left;'})
    for row in classes:
        Path("images/classes").mkdir(parents=True, exist_ok=True)
        r = requests.get(row['src'])
        path = Path("images/classes/")
        file = row['alt']+".png"
        fpath = (path / file)
        
        with fpath.open('wb') as f:
            f.write(r.content)
            bar() # For bar
            
def installskills():
    headers = {
        'User-Agent': 'Ping-Untrusted-Asset-Scraper v.1.10',
        'From': 'Ping#6175'  
    }
    URL = "https://www.playuntrusted.com/manual/skills/"
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html5lib')

    skills_table = soup.find("div", {"id": "skillstable"})
    skill_divs = skills_table.find_all("div", {"style": "float:right;"})
    skills = []
    for skill_div in skill_divs:
        h1_tag = skill_div.find_previous_sibling('div').find('h1')
        img_tag = skill_div.find('img')
        if h1_tag is not None and img_tag is not None:
            skill_name = h1_tag.text.strip()
            img_src = img_tag.get('src')
            skills.append({"name": skill_name, "img_url": img_src})

    if skills:
        for skill in skills:
            Path("images/skills").mkdir(parents=True, exist_ok=True)
            r = requests.get(skill['img_url'])
            
            path = Path("images/skills/")
            file = skill['name']+".png"
            fpath = (path / file)
            
            with fpath.open('wb') as f:
                f.write(r.content)
                bar() # For bar

def installavatars():
    headers = {
        'User-Agent': 'Ping-Untrusted-Asset-Scraper v.1.10',
        'From': 'Ping#6175'  
    }
    avatar = 1
    fail = 0
    urls = []
    while True:
        url = "https://eu01.playuntrusted.com/avatars/{:05d}.png".format(avatar)
        r = requests.get(url, headers=headers)

        if fail > 20:
            bar() # For bar
            break
        if r.ok:
            urls.append(url)
            Path("images/avatars").mkdir(parents=True, exist_ok=True)
            with open("images/avatars/{:05d}.png".format(avatar), "wb") as f:
                f.write(r.content)
                bar() # For bar
        else:
            bar() # For bar
            fail +=1 # for some reason some numbers are skipped??? thanks untrusted very nice and sweet.
        avatar += 1


print("Installing assets...")
with alive_bar(367) as bar: # The 367 is the number of bar hits, check bar hits regularly.
    installclasses()
    installskills()
    installavatars()


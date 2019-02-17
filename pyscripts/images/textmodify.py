str = "https://www.govtrack.us/static/legislator-photos/"
strend = "-200px.jpeg"
numchar = 27

import re
g = open('images.txt','w', encoding='utf-8')

with open('links.txt','r', encoding='utf-8') as f:
    for x in f:
        x = x.rstrip()
        x = re.sub(r'\s+', '', x)
        ind = x.find('/',27)
        g.write(str + x[ind+1:ind+7] + strend + "\n")
f.close()
g.close()

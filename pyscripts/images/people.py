str = "https://www.govtrack.us/static/legislator-photos/"
strend = "-200px.jpeg"
numchar = 27

import re
g = open('people.txt','w', encoding='utf-8')

with open('links.txt','r', encoding='utf-8') as f:
    for x in f:
        x = x.rstrip()
        x = re.sub(r'\s+', '', x)
        ind = x.find('/',25)
        ind2 = x.find('/',27)
        names = x[ind+1:ind2]
        names = re.sub('_', ' ', names)
        g.write(names+"\n")
f.close()
g.close()

import re
g = open('links.txt','w', encoding='utf-8')

with open('site.txt','r', encoding='utf-8') as f:
    for x in f:
        x = x.rstrip()
        x = re.sub(r'\s+', '', x)
        if (x.startswith("<ahref")):
            g.write(x+"\n")

f.close()
g.close()

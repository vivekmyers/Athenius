
g = open('imagedb.csv','w', encoding='utf-8')

with open("people.txt") as f1, open("images.txt") as f2:
  for x, y in zip(f1, f2):
     z = "{0}, {1}".format(x.rstrip(), y.rstrip())
     g.write(z + "\n")

f1.close()
f2.close()
g.close()

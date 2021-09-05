from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

r = open('data.html','r')
soup = BeautifulSoup(r, 'html5lib')

soup.prettify()
# print(type(soup.prettify()))
new_file = open('pretty.html','w')
new_file.write(soup.prettify())

name_list = soup.findAll('span', attrs = {'class':'jsx-1259716541 desktop--only pointer'})
name = [company.text for company in name_list]

cap = soup.find_all('span', attrs = {'class':"jsx-1411633368 data-cell screener-cell ellipsis"})
rowid=[row.get('data-row') for row in cap]
final_rows = []
idx = 0
abbr={}
for id in rowid:
    marcap = soup.findAll('span', attrs = {'class':'jsx-1411633368 data-cell screener-cell', 'data-row':id})
    market_cap ,close_price ,pe ,growth5Y ,alpha ,beta = marcap[0].text, marcap[1].text, marcap[2].text, marcap[3].text, marcap[4].text, marcap[5].text 
    d = dict(
        name=name[idx],
        market_cap = market_cap ,
        close_price = close_price ,
        pe = pe ,
        growth5Y = growth5Y ,
        alpha = alpha ,
        beta = beta
    )
    if '-' == d.get("beta"):
        continue
    elif  (float(d.get('beta'))<=1.0 and float(d.get('alpha'))>=0.0):
        final_rows.append(d)
        abbr[id] = name[idx]
        idx+=1

filename = 'processed_data.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['name','market_cap' ,'close_price' ,'pe' ,'growth5Y' ,'alpha' ,'beta'])
    w.writeheader()
    for row in final_rows:
        w.writerow(row)

x = [float(row.get('alpha')) for row in final_rows]
y = [float(row.get('beta')) for row in final_rows]
# fig, scatter = plt.subplots()
plt.scatter(x,y)
for i,txt in enumerate(abbr.keys()):
    plt.annotate(txt, (x[i],y[i]))

y_lim = list(plt.ylim())
x_lim = list(plt.xlim())
print(x_lim,y_lim)
plt.plot([-0.1,y_lim[0]], [0,1], 'k-', color = 'r')
plt.plot(x_lim, [1,1], 'k-', color = 'r')
plt.ylim(y_lim)
plt.xlim(x_lim)

plt.show()
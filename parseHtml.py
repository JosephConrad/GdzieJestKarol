from BeautifulSoup import *
import urllib2
import json
import sqlite3

url = "http://m.ztm.waw.pl/rozklad_nowy.php?c=182&l=1#content"
webFile = urllib2.urlopen(url).read()
 
html = webFile
parsed_html = BeautifulSoup(html)

def getParsedData(url, cursor):
    webFile = urllib2.urlopen(url).read()
    html = webFile
    parsed_html = BeautifulSoup(html)

    directions = {}
    for table in parsed_html.body.findAll('table'): 
        reDirection = '<strong>(.*?)</strong>'
        direction = re.search(reDirection, str(table)).group(1)
        stops = []
        for tr in table.findAll('tr'): 
            try:
                regex = '<a href="(.*?)" class="(.*?)">(.*?)</a>'
                nz = (int)(re.search(regex, str(tr)).group(2) == "nz")
                st = re.search(regex, str(tr)).group(3)
                regexOp = 'class="op">(.*?)</td>'
                nr = re.search(regexOp, str(tr)).group(1)
                stops.append((nz, st, nr))
            except:
                pass
        directions[direction] = stops
    return directions

findRegex = 'q=(.*?)#'
linesNumbers = []
lines = dict()

for div in parsed_html.body.findAll('a'): 
    try:
        linesNumbers.append(re.search(findRegex, str(div)).group(1))
    except:
        pass

conn = sqlite3.connect('lines.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE lines (ID INTEGER PRIMARY KEY, name TEXT)''')
cursor.execute('''CREATE TABLE diractions (ID INTEGER PRIMARY KEY, name TEXT)''')

for line in linesNumbers[:10]:
    cursor.execute("INSERT INTO lines (name) VALUES ('%s')" % line)
    url = "http://m.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&q=%s#content" % line
    lines[line] = getParsedData(url, cursor.lastrowid, cursor)

conn.commit()
conn.close()

with open('lines.json', 'w') as fp:
    json.dump(lines, fp, indent=4)


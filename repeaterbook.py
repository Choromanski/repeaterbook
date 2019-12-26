from bs4 import BeautifulSoup
import requests, csv

URL = "https://www.repeaterbook.com/repeaters/index.php?state_id="

page_response = requests.get(URL + "none")

soup = BeautifulSoup(page_response.content, "html.parser").findAll("table")[3]

state = {}
for a in soup.findAll('a', href=True):
	state[a['href'].strip()[-2:]] = a.contents[0].strip()

print("States")
for i in state:
	print(i + ") " + state[i])

state_id = int(input("Selection ID: "))

print(state[str(state_id).zfill(2)])

page_response = requests.get(URL + str(state_id).zfill(2))

print("1) Nearest city/town\n2) County")

search = int(input("Selection ID: "))

if search == 1:
	soup = BeautifulSoup(page_response.content, "html.parser").findAll("a", {'href': lambda L: L and L.startswith('location_search.php?state_id=' + str(state_id).zfill(2) + '&type=city&loc=')})
elif search == 2:
	soup = BeautifulSoup(page_response.content, "html.parser").findAll("a", {'href': lambda L: L and L.startswith('location_search.php?type=county&state_id=' + str(state_id).zfill(2) + '&loc=')})

location = {}
count = 0
for i in soup:
	location[str(count)] = {'href': i['href'], 'name':i.text}
	count += 1

for i in location:
	print(i + ') ' + location[i]['name'])

loc = int(input("Selection ID: "))

print(location[str(loc)]['name'])

page_response = requests.get('https://www.repeaterbook.com/repeaters/' + location[str(loc)]['href'])

soup = BeautifulSoup(page_response.content, "html.parser").findAll("table")[2]

count = 1
output_rows = []
for table_row in soup.findAll('tr'):
	columns = table_row.findAll('td')
	output_row = []
	for column in columns:
		output_row.append(column.text.replace('\n', ' ').strip())
	if len(output_row) > 4:
		output_row.pop()
		temp = [count, output_row[3].upper().replace(',', ''), output_row[0], output_row[1][0], output_row[1][1:].replace(' MHz', ''), "Tone", output_row[2].split(' /')[0], 88.5, 23, "NN", "FM", 5, '', '', '', '', '', '']
		output_rows.append(temp)
		count += 1

with open('output.csv', 'w+', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Location', 'Name', 'Frequency', 'Duplex', 'Offset', 'Tone', 'rToneFreq', 'cToneFreq', 'DtcsCode', 'DtcsPolarity', 'Mode', 'TStep', 'Skip', 'Comment', 'URCALL', 'RPT1CALL', 'RPT2CALL', 'DVCODE'])
	writer.writerows(output_rows)

print("output.csv created.")

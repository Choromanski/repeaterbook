from bs4 import BeautifulSoup
import requests, csv

URL = "https://www.repeaterbook.com/repeaters/index.php?state_id="

page_response = requests.get(URL + "none")

soup = BeautifulSoup(page_response.content, "html.parser").findAll("table")[3]

state = {}
for a in soup.findAll('a', href=True):
	state[a['href'].rstrip()[-2:]] = a.contents[0].rstrip()

print("States")
for i in state:
	print(i + ") " + state[i])

state_id = int(input("Selection ID: "))

print(state[str(state_id).zfill(2)])

page_response = requests.get(URL + str(state_id).zfill(2))
#print(page_response.content)

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
#page_response = requests.get('https://www.repeaterbook.com/repeaters/' + 'location_search.php?type=county&state_id=42&loc=Bucks')

soup = BeautifulSoup(page_response.content, "html.parser").findAll("table")[2]

print(soup)


from bs4 import BeautifulSoup
from urllib2 import HTTPError, urlopen
import codecs
import re

def month_to_number(month):
	if month == 'January':
		return '01'
	if month == 'February':
		return '02'
	if month == 'March':
		return '03'
	if month == 'April':
		return '04'
	if month == 'May':
		return '05'
	if month == 'June':
		return '06'
	if month == 'July':
		return '07'
	if month == 'August':
		return '08'
	if month == 'September':
		return '09'
	if month == 'October':
		return 10
	if month == 'November':
		return 11
	if month == 'December':
		return 12

def fix_day(day):
	if len(day) == 1:
		return "0"+str(day)
	else:
		return str(day)

def clear_spaces(string):
	return string.replace('\t\t', ' ').replace('\t', ' ').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()

def strip_phrases(string):
	phrases = ['First District--Boston', 'Second District--New York', 'Third District--Philadelphia', 'Fourth District--Cleveland', 'Fifth District--Richmond', 'Sixth District--Atlanta', 'Seventh District--Chicago', 'Eighth District--St. Louis', 'Ninth District--Minneapolis', 'Tenth District--Kansas City', 'Eleventh District--Dallas', 'Twelfth District--San Francisco']

	for p in phrases:
		string = string.replace(p, '')
	return string


url = 'http://www.federalreserve.gov/monetarypolicy/beigebook/default.htm'
html_data = urlopen(url).read()

p = re.compile('beigebook[\d][\d][\d][\d][\d][\d].htm')
pages = p.findall(html_data)

parsed_html = BeautifulSoup(html_data)
counter = {}
new_urls = {}
old_urls = {}
for a in parsed_html.find_all('a'):
	if a.text[0:12] == 'Beige Book -':
		if a.text in counter:
			pass
		else:
			counter[a.text] = 1
			date = a.text.replace('Beige Book - ', '')
			#print a.text
			#print date
			year = date.split(',')[1].strip()
			month = month_to_number(date.split(',')[0].split(' ')[0].strip())
			day = fix_day(date.split(',')[0].split(' ')[1].strip())
			
			url = ''

			if int(year) >= 2011:
				if month == '03' and year == '2011':
					url = 'http://www.federalreserve.gov/monetarypolicy/beigebook/beigebook20110302.htm'
				else:
					url = 'http://www.federalreserve.gov/monetarypolicy/beigebook/beigebook'+str(year)+str(month)+'.htm'
				new_urls[url] = [year, month, day]
			else:
				url = 'http://www.federalreserve.gov/fomc/beigebook/'+str(year)+'/'+str(year)+str(month)+str(day)+'/FullReport.htm'
				old_urls[url] = [year, month, day]

output = codecs.open('output.csv', encoding='utf-8', mode='w')

output.write('location|year|month|text\n')

for url in new_urls:
	print url

	year = new_urls[url][0]
	month = new_urls[url][1]
	day = new_urls[url][2]


	html_data = urlopen(url).read()
	parsed_html = BeautifulSoup(html_data)

	summary = parsed_html.body.find('div', attrs={'id':'div_summary'})
	boston = parsed_html.body.find('div', attrs={'id':'div_boston'})
	new_york = parsed_html.body.find('div', attrs={'id':'div_new_york'})
	philadelphia = parsed_html.body.find('div', attrs={'id':'div_philadelphia'})
	cleveland = parsed_html.body.find('div', attrs={'id':'div_cleveland'})
	richmond = parsed_html.body.find('div', attrs={'id':'div_richmond'})
	atlanta = parsed_html.body.find('div', attrs={'id':'div_atlanta'})
	chicago = parsed_html.body.find('div', attrs={'id':'div_chicago'})
	st_louis = parsed_html.body.find('div', attrs={'id':'div_st_louis'})
	minneapolis = parsed_html.body.find('div', attrs={'id':'div_minneapolis'})
	kansas_city = parsed_html.body.find('div', attrs={'id':'div_kansas_city'})
	dallas = parsed_html.body.find('div', attrs={'id':'div_dallas'})
	san_francisco = parsed_html.body.find('div', attrs={'id':'div_san_francisco'})

	locations = {'summary': summary, 'new_york': new_york, 'boston': boston, 'philadelphia': philadelphia, 'cleveland': cleveland, 'richmond': richmond, 'atlanta': atlanta, 'chicago': chicago, 'st_louis': st_louis, 'minneapolis': minneapolis, 'kansas_city': kansas_city, 'dallas': dallas, 'san_francisco': san_francisco}

	for location in locations:
		#for cat in locations[location].find_all(re.compile(r"strong")):
			#for cat_parent in cat.find_parents("p"):
		#text = unicode(locations[location].text.replace(cat.text.strip(), '').replace('\n', ''))
		text = unicode(clear_spaces(locations[location].text.replace('\n', '')))
		output_text = str(location)+'|'+str(year)+'|'+str(int(month))+'|'+unicode(strip_phrases(text).strip())
		#print output_text
		output.write(output_text+'\n')
		#output.write(str(location)+'|'+unicode(cat.text.strip())+'|'+str(year)+'|'+str(int(month))+'|'+unicode(text.strip())+'\n')


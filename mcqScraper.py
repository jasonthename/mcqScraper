from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def mcq(mcqLinks):
	temp = set()
	for link in mcqLinks:
		try:
			html = urlopen(link)
		except HTTPError as e:
			print ('Error Opening Page')
			return None
		try:
			bsObj = BeautifulSoup(html)
			newLinks = bsObj.findAll('a', href=re.compile(link))
		except AttributeError as e:
			return None

		temp1 = set()
		for item in newLinks:
			temp1.add(item.attrs['href'])

		temp = temp.union(temp1)

	mcqLinks =  sorted(mcqLinks.union(temp))
	
	mcqSets = defaultdict(list)
	
	for link in mcqLinks:
		try:
			html = urlopen(link)
		except HTTPError as e:
			print ('Error Opening Page')
			return None
		try:
			bsObj = BeautifulSoup(html)
			headings = bsObj.findAll('h2')
		except AttributeError as e:
			return None
		lst = []
		for item in headings:
			temp = item.find('a')
			if temp:
				lst.append(temp.attrs['href'])
		
		var = link.split('/')
		if var[-2] == 'page':
			mcqSets[var[-3]].append(lst)
		else:
			mcqSets[var[-1]].append(lst)

	for key, value in mcqSets.items():
		for links in value:
			for link in links:
				fhand = open(key+'.txt', 'a')
				fhand.write('\n')
				try:
					html = urlopen(link)
				except HTTPError as e:
					print ('Error Opening Page')
					return None
				try:
					bsObj = BeautifulSoup(html)
					data = bsObj.findAll('p')
					ans = bsObj.find('div', {'class':'collapseomatic_content'})
				except AttributeError as e:
					return None
				if 'Related' in data[11].get_text():
					data = data[:10]
				else:
					data = data[2:12]
				ans = ans.get_text().strip().split('/')
				fhand.write('\n' + link.split('/')[-1] + '\n')
				for i in range(len(data)):
					fhand.write('\n')
					fhand.write(data[i].get_text())
					fhand.write('\nAnswer:'+ans[i].split('–')[-1])
					fhand.write('\n')
				fhand.close()

def main():
	try:
		html = urlopen("http://mcqquestions.com/")
	except HTTPError as e:
		print ('Error Opening Page')
		return None
	try:
		bsObj = BeautifulSoup(html)
		Links = bsObj.findAll('a', href=re.compile('(/category/)'))
	except AttributeError as e:
		return None

	queLinks = set()
	for item in set(Links):
		queLinks.add(item.attrs['href'])

	mcqLinks = set()

	for item in queLinks:
		if 'objective' in item or 'mcq' in item.split('/')[-1]:
			mcqLinks.add(item)
	
	mcq(mcqLinks)
	
if __name__ == '__main__':
	main()
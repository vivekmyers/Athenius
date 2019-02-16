import requests
from xml.etree import ElementTree

def constructSessionURL(year):
	res =  "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_" + str(senateNumber) + "_" + str(sessionNumber) + ".xml"
	print (res)
	return res

def outputSessionPath(senateNumber, sessionNumber):
	return "data/Senate/Session/"+str(senateNumber)+"_"+str(sessionNumber)+".xml"

def constructVoteURL(year, voteNumber):
	res = "http://clerk.house.gov/evs/"+ str(year) +"/roll"+str(voteNumber).zfill(3)+".xml"
	print (res)
	return res

def outputVotePath(year, voteNumber):
	return "data/House/Votes/"+str(year)+"_"+str(voteNumber)+".xml"

# Quick hack to bypass webscrape blocker with header:
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}


for year in range(2018, 2010, -1):

	vote = 1

	return_code = 503

	while return_code != 404:

		URL = constructVoteURL(year, vote)

		response = requests.get(URL, headers=headers)
		print (response)
		return_code = response.status_code
		if return_code == 200:
			with open(outputVotePath(year, vote), 'wb') as file:
				file.write(response.content)
		vote += 1

'''
proxy_dict = {
    'http': 'socks5://localhost:4022',
    'https': 'socks5://localhost:4022',
}'''

'''

for senateNumber in range(116, 110, -1):
	for sessionNumber in range(1, 3):
		if not(senateNumber == 116 and sessionNumber == 2):

			URL = constructSessionURL(senateNumber, sessionNumber)

			return_code = 503
			attempt = 0
			while return_code != 200 and attempt < 5:
				response = requests.get(URL, headers=headers, proxies=proxy_dict)
				print (response)
				return_code = response.status_code
				attempt += 1

			if return_code == 200:
				with open(outputSessionPath(senateNumber, sessionNumber), 'wb') as file:
					file.write(response.content)

				root = ElementTree.fromstring(response.content)
				max_votes = len(root[3])
				print (max_votes)

				for voteNumber in range(1, max_votes+1):

					URL = constructVoteURL(senateNumber, sessionNumber, voteNumber)

					return_code = 503
					attempt = 0
					while return_code != 200 and attempt < 5:
						response = requests.get(URL, headers=headers, proxies=proxy_dict)
						print (response)
						return_code = response.status_code
						attempt += 1

					if return_code == 200:
						with open(outputVotePath(senateNumber, sessionNumber, voteNumber), 'wb') as file:
							file.write(response.content)
'''
import requests
from xml.etree import ElementTree

# returns string URL to senate.gov xml file based on senateNumber and sessionNumber
def constructSessionURL(senateNumber, sessionNumber):
	res =  "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_" + str(senateNumber) + "_" + str(sessionNumber) + ".xml"
	print (res)
	return res


# returns string path to local xml file based on input senateNumber and sessionNumber.
def outputSessionPath(senateNumber, sessionNumber):
	return "data/Senate/Session/"+str(senateNumber)+"_"+str(sessionNumber)+".xml"


# returns string URL to senate.gov bill vote xml file based on senateNumber, sessionNumber, and voteNumber
def constructVoteURL(senateNumber, sessionNumber, voteNumber):
	res = "https://www.senate.gov/legislative/LIS/roll_call_votes/vote"+str(senateNumber) + str(sessionNumber) + "/vote_" + str(senateNumber) + "_" + str(sessionNumber) + "_" + str(voteNumber).zfill(5) + ".xml"
	print (res)
	return res


# returns string path to local xml file based on input senateNumber, sessionNumber, and voteNumber.
def outputVotePath(senateNumber, sessionNumber, voteNumber):
	return "data/Senate/Votes/"+str(senateNumber)+"_"+str(sessionNumber)+"_"+str(voteNumber)+".xml"


# Quick hack to bypass webscrape blocker with header:
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

# Use proxy if whitelisted:
proxy_dict = {
    'http': 'socks5://localhost:4022',
    'https': 'socks5://localhost:4022',
}


# if script crashes due to connection err, change resume_year and resume_vote
# so that the script can pick up from where it left off
resume_senateNumber = 115
resume_sessionNumber = 1
resume_voteNumber = 100


for senateNumber in range(116, 110, -1):
	for sessionNumber in range(1, 3):

		if senateNumber == resume_senateNumber:
			sessionNumber = resume_sessionNumber

		if senateNumber <= resume_sessionNumber:
			if not(senateNumber == 116 and sessionNumber == 2):

				URL = constructSessionURL(senateNumber, sessionNumber)	# construct URL to senate voting history

				return_code = 503
				attempt = 0
				# Try to load xml up to 5 times
				while return_code != 200 and attempt < 5:
					response = requests.get(URL, headers=headers, proxies=proxy_dict)
					print (response)
					return_code = response.status_code
					attempt += 1

				# return_code = 200 if .xml query was successful
				if return_code == 200:
					with open(outputSessionPath(senateNumber, sessionNumber), 'wb') as file:
						file.write(response.content)

					root = ElementTree.fromstring(response.content)
					max_votes = len(root[3])	# calculate number of votes in session
					print (max_votes)

					startVoteNumber = 1
					if senateNumber == resume_senateNumber and sessionNumber == resume_sessionNumber:
						startVoteNumber = resume_voteNumber

					# download each .xml corresponding to each vote taken in senate
					for voteNumber in range(startVoteNumber, max_votes+1):

						# construct URL to vote data for a specific bill
						URL = constructVoteURL(senateNumber, sessionNumber, voteNumber)

						return_code = 503
						attempt = 0

						# Try to load xml up to 5 times
						while return_code != 200 and attempt < 5:
							response = requests.get(URL, headers=headers, proxies=proxy_dict)
							print (response)
							return_code = response.status_code
							attempt += 1

						# if xml loaded successfully, save file locally
						if return_code == 200:
							with open(outputVotePath(senateNumber, sessionNumber, voteNumber), 'wb') as file:
								file.write(response.content)

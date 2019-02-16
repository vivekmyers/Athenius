import requests

def constructSessionURL(senateNumber, sessionNumber):
	return "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_" + senateNumber + "_" + sessionNumber + ".xml"

def constructVoteURL(senateNumber, sessionNumber, voteNumber):
	return "https://www.senate.gov/legislative/LIS/roll_call_votes/vote"+setnateNumber + sessionNumber + "/vote_" + senateNumber + "_" + sessionNumber + "_" + voteNumber + ".xml"

response = requests.get(URL)
with open('../data/vote_116_1_00023.xml', 'wb') as file:
	file.write(response.content)
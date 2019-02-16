import requests

# returns string URL to house.gov xml file based on input year and note number.
def constructVoteURL(year, voteNumber):
	res = "http://clerk.house.gov/evs/"+ str(year) +"/roll"+str(voteNumber).zfill(3)+".xml"
	print (res)
	return res

# returns string path to local xml file based on input year and note number.
def outputVotePath(year, voteNumber):
	return "data/House/Votes/"+str(year)+"_"+str(voteNumber)+".xml"


# Quick hack to bypass webscrape blocker with header:
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

# if script crashes due to connection err, change resume_year and resume_vote
# so that the script can pick up from where it left off
resume_year = 2013
resume_vote = 617

for year in range(2018, 2010, -1):

	vote = 1

	if year == resume_year:
		vote = resume_vote

	if year <= resume_year:
		return_code = 503

		# return_code = 404 when vote > max_vote of session
		while return_code != 404:

			URL = constructVoteURL(year, vote)

			response = requests.get(URL, headers=headers)
			print (response)
			return_code = response.status_code
			if return_code == 200:
				# only save .xml if request was a success
				with open(outputVotePath(year, vote), 'wb') as file:
					file.write(response.content)
			vote += 1
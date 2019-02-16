from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import numpy as np

def senate_records():
    '''
    Get Senate records as described below.
    '''
    return get_all_voting_records('../data/Senate/Votes', 'senate')

def house_records():
    '''
    Get House records as described below.
    '''
    return get_all_voting_records('../data/House/Votes', 'house')

def get_all_voting_records(loc, kind):
    '''
    Takes in a data location consisting containing only xml files with
    individual house vote results or senate vote results.
    Kind is either 'house' or 'senate,' based on what data is being read.
    Returns tuple (arr, reps, bills) where
        arr[i][j] == 0 indicates reps[i] voted Nay on bills[j]
        arr[i][j] == 1 indicates reps[i] voted Yea on bills[i]
        arr[i][j] == -1 indicates reps[i] did not vote on bills[j].
    Bills are represented as (congress, session, vote_number) tuples.
    Representatives are denoted by a string with their name, party, and state.
    '''
    
    voting_records = {} # map from representatives to maps from bills to votes
    all_bills = []
    house = kind == 'house'
    
    # iterate over xml files in target dir
    for i in [x for x in listdir(loc)
              if x[-4:] == '.xml']:
        try:
            tree = ET.parse(f'{loc}/{i}').getroot()
            if not house:
                bill = tuple(tree.find(x).text
                         for x in ['congress', 'session', 'vote_number'])
            else:
                tmp = tree.find('vote-metadata')
                bill = tuple(tmp.find(x).text
                         for x in ['congress', 'session', 'rollcall-num'])
        except:
            print(f'Unable to read {i}')
            continue
        # record bill, then add every vote to voting_records dict
        all_bills.append(bill)
        for member in tree.find('members' if not house else 'vote-data'):
            if house:
                rep = member.find('legislator').text
                attr = member.find('legislator').attrib
                rep = f'{rep} ({attr["party"]}-{attr["state"]})'
            else:
                rep = member.find('member_full').text
            try:
                choice = ['Nay', 'Yea'].index(
                    member.find('vote' if house else 'vote_cast').text)
            except ValueError:
                choice = -1
            if rep not in voting_records:
                voting_records[rep] = {}
            voting_records[rep][bill] = choice
            
    num_reps = len(voting_records)
    num_bills = len(all_bills)
    bill_to_int = {v: i for i, v in enumerate(all_bills)} # for efficiency
    # make an array representation
    arr = np.zeros([num_reps, num_bills])
    col = sorted(i for i in voting_records)
    
    for i, (rep, votes) in enumerate(sorted([x for x in voting_records.items()],
                                 key=lambda x: x[0])):
        for bill in votes:
            arr[i][bill_to_int[bill]] = votes[bill]
            
    return arr, col, all_bills



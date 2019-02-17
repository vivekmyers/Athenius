from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import numpy as np
import sys
import pickle
import pandas as pd

def senate_records(cached=False):
    '''
    Get Senate records as described below.
    If cached is set, use serialized copy.
    '''
    if cached:
        return pickle.load(open('senate_records.p', 'rb'))
    else:
        result = get_all_voting_records('../data/Senate/Votes', 'senate')
        pickle.dump(result, open('senate_records.p', 'wb'))
        return result

def house_records(cached=False):
    '''
    Get House records as described below.
    If cached is set, use serialized copy.
    '''
    if cached:
        return pickle.load(open('house_records.p', 'rb'))
    else:
        result = get_all_voting_records('../data/House/Votes', 'house')
        pickle.dump(result, open('house_records.p', 'wb'))
        return result

def get_all_voting_records(loc, kind):
    '''
    Takes in a data location consisting containing only xml files with
    individual house vote results or senate vote results.
    Kind is either 'house' or 'senate,' based on what data is being read.
    Returns tuple (arr, reps, bills) where
        arr[i][j] == 0 indicates reps[i] voted Nay on bills[j]
        arr[i][j] == 1 indicates reps[i] voted Yea on bills[i]
        arr[i][j] == -1 indicates reps[i] did not vote on bills[j].
    Bills are represented as dictionaries with date, result, subject, etc. attributes.
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
                bill = frozenset({x: tree.find(x).text
                         for x in ['congress', 'session', 'vote_number', 'congress_year', 'vote_date',
                             'vote_question_text', 'vote_document_text', 'vote_result_text', 
                             'question', 'vote_title', 'majority_requirement', 'vote_result']}.items())
            else:
                tmp = tree.find('vote-metadata')
                bill = frozenset({x: tmp.find(x).text
                         for x in ['majority', 'congress', 'session', 'rollcall-num', 'legis-num', 
                             'vote-question', 'vote-type', 'vote-result', 'action-date', 'action-time', 
                             'vote-desc']}.items())
        except:
            print(f'Unable to read {i}', file=sys.stderr)
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
                    member.find('vote' if house else 'vote_cast').text) * 2 - 1
            except ValueError:
                choice = 0
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
            
    nominate_table = pd.read_csv('../data/nominate.csv')
    processed = {a[0] + a[1:].split(',')[0].lower() + f' ({"R" if party_code == 200 else "D" if party_code == 100 else "I"}-{state_abbrev})': 
                    (b, c) for _, a, b, c, state_abbrev, party_code in 
                    nominate_table[['bioname', 'nominate_dim1', 'nominate_dim2', 'state_abbrev', 'party_code']].itertuples()}
    return arr, np.array([(i, processed[i][0], processed[i][1]) 
                            for i in col if i in processed]), np.array([dict(x) for x in all_bills])



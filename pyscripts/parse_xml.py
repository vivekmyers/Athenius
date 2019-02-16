from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

def get_all_voting_records():
    congresspeople = {}
    for i in [x for x in listdir('../data') if x[-4:] == '.xml']
        tree = ET.parse(i)
        for 


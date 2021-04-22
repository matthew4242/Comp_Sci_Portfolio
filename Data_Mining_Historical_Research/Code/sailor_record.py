# -*- coding: utf-8 -*-
"""

@author: mah60
"""

from pprint import pprint
import matplotlib
matplotlib.use('Agg')

from datetime import datetime

class Sailor:
    """
    Object used to help store and return data in an effiecient way.
    Will take sailor primary key values, name, year of birth(yob), 
    place of birth(pob). As well, as the newly generated ID.
    
    Able to store records inside if required.
    """
    def __init__(self, id_s, name,yob,pob):
        self.id = id_s
        self.name = name
        self.records = []
        self.yob = yob
        self.pob = pob
        
    def add_record(self, record):
        self.records.append(record)
    
    def get_records(self):
        return self.records
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_pob(self):
        return self.pob
    
    def get_yob(self):
        return self.yob

def crew_memb_promotion_track(db):
    """
    Will perform 3 stages;
        1. gather sailor data
        2. present selection menu
        3. print sailor timeline
    
    The timeline will represent the x sailor work/promotion track
    
    ags => db - db.col - the database collection
    return => None
    """
    # gather sailor data
    sailors = get_sailors(db)
    # present selection menu
    sailor_id = sailor_selection(db, sailors)
    
    # find matches 
    results = db.aggregate([{"$unwind": "$mariners"},
                            {"$match": {"mariners.name": sailors[sailor_id].get_name(),
                                        "mariners.year_of_birth": sailors[sailor_id].get_yob(),
                                        "mariners.place_of_birth": sailors[sailor_id].get_pob()}}])
    # find dates and order dates
    # create array of items found
    for item in results:
        #pprint(item)
        sailors[sailor_id].add_record(item)
        # test 45818 thomas williams
    # sort join date 
    records = sailors[sailor_id].get_records()
    #create array [id, date] and [id, record]
    dates = []
    record_array = []
    date_time_formats = ['%Y-%m-%d', '%b %d %Y %I:%M%p', '%Y-%m-%d %I:%M:%S']
    for i, r in enumerate(records):
        # check if date is valed and convert it
        pass_on = False
        r_date = None
        for dtf in date_time_formats:
            if(not pass_on):
                pass_on, r_date = validate_date(r['mariners']['this_ship_joining_date'], dtf )
        if(not pass_on): # still not found put defualt value to remove uncalculated values
            r_date = datetime.now()
        dates.append([i,r_date])
        record_array.append([i, r])
    # get ordered dates
    ordered_dates = order_dates(dates)
    # print out records in order
    print("------------------------------------------------------------")
    print("Promotion Rank For: {}".format(sailors[sailor_id].get_name()))
    print("------------------------------------------------------------")
    for i, od in enumerate(ordered_dates):
        for ra in record_array:
            if(od[0] == ra[0]):
                 # we want joining date - leaving date - name - ship - capcity
                 pprint("Joining date: {}, Leaving date: {}, Ship: {}, Capacity: {}".format(
                         ra[1]['mariners']['this_ship_joining_date'],
                         ra[1]['mariners']['last_ship_leaving_date'],
                         ra[1]['vessel name'],
                         ra[1]['mariners']['this_ship_capacity']))
                 if(i != len(ordered_dates) - 1):
                     print("------------------------------------------------------------")
                     print('-> next stage on timeline ->')
                     print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    
def get_sailors(db):
    """
    Will gather the data about individual sailors, collect data from given collection. 
    Then place them into a dict of objects that is catagorised by the ID system.

    ags => db - db.col - the database collection
    return => sailors - Dictionary - Dict[ID] = {<sailor object>}
    """
    # get unique sailor infomation
    result = db.aggregate([{"$unwind": "$mariners"},
                           {"$group": { "_id": {
            'name': "$mariners.name",
            'year_of_birth': "$mariners.year_of_birth",
            'place_of_birth': "$mariners.place_of_birth"
            }}}])
    id_count = '1'
    sailors = {}
    # transform to sailor objects
    for record in result:
        sailors[id_count] = Sailor(id_count, record["_id"]["name"], 
            record["_id"]["year_of_birth"], 
            record["_id"]["place_of_birth"])
        id_count = str(int(id_count) + 1)
        
#    for s in sailors:
#        print(sailors[s].get_id())

    return sailors

def sailor_selection(db, sailors):
    """
    Allow for user input to select a specific sailor, can enter 's' to
    get to the search menu.
    
    selection process will be specified sailor ID
    
    ags => db - db.col - the database collection
            sailors - Dictionary - Dict[ID] = {<sailor object>}
    return => sailor_id
    """
    while True:  # ask until ID value is entered
        n_input = input("Enter Sailor ID: enter 's' to search names : ")
        if(n_input.isdigit()): # make sure ID is integer
            if(int(n_input) > 0 and int(n_input) <= len(sailors)): # make sure value is within range
                sailor_id = sailors[n_input].get_id() # once got sailor return ID
                break
        elif(n_input.lower() == 's'):  # go to search menu
            search_names(sailors)     # return when done
        n_input = "" # reset the input
    return sailor_id

def search_names(sailors):
    """
    Search sailors for names and their corrisponding values. Exit when done, 
    to enter the values.
    
    args => sailors - Dictionary - Dict[ID] = {<sailor object>}
    return => None
    """
    print("-------------------------------------------")
    print("You have entered name search engine")
    print("-------------------------------------------")
    while True:  # loop through search code till 'esc42'
        print("-------------------------------------------")
        n_input = input("Enter name or starting characters for search\n type 'esc42' to exit : ")
        print("-------------------------------------------")
        if(n_input.lower() == 'esc42'): # if input 'esc42' exit while loop
            break
        else:
            for s in sailors: # check if input is in sailor names
                if(str(n_input) in sailors[s].get_name()): # print out details of matching sailors
                    pprint("Id: {}, Name: {}, Year of Birth: {}, Place of Birth: {}".format(
                            sailors[s].get_id(), sailors[s].get_name(),
                            sailors[s].get_yob(), sailors[s].get_pob()))
    
    
    
def order_dates(dates):
    """
    Order the date values and matchs ID for individual dates
    
    args => dates - list[list] - [[ID, date]]
    return => new_dates - list[list] - [[ordered_ID, date]]
    """
    # create date array
    date_array = []
    for d in dates:
        date_array.append(d[1])
    date_array.sort()
    # reconnect id
    new_dates = []
    used_id = [] # make sure no replica ids produced
    for da in date_array:
        for d in dates:
            if(da == d[1]):
                # make sure ID not already used
                if(d[0] not in used_id):
                    new_dates.append([d[0], d[1]])
                    used_id.append(d[0])
    return new_dates

def validate_date(date, format_string):
    """
    Checks if data is valid
    
    args => date - string - string of date value
            format_date - string - format that the date is being transformed into
    return => boolean - True - data been accepted
              new_date - datetime - datetime object if accepted, if not value will be None
    """
    try: 
        new_date = datetime.strptime(date, format_string)
        return True, new_date
    except ValueError:
        return False , None
    
    
    
    
    
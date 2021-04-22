# -*- coding: utf-8 -*-
"""
@author: mah60
"""

from pymongo import MongoClient
import matplotlib
matplotlib.use('Agg')

import ship_filter as f
import prop_rank as pr
import sailor_record as sr
import hist_crew_size as hcs
import top_visits as tv 
      
    
def menu(db):
    """
    This function will control the application and will call the different
    functions through the use of a menu. Selection process is though integers.
    
    ags => db - db.col - the database collection
    return => None
    """    
    # print menu until exited
    while True:
        print("-------------------------------------------")
        print("1. Proportion of individuals at each rank")
        print("2. Promotion tracking of a individual")
        print("3. Histogram of number of crew on each ship")
        print("4. Number of ship visits to each port that isn't Aberystwth")
        print("5. Exit application")
        print("-------------------------------------------")
        # ask for input
        m_input = input("Please enter ID for menu selection: \ne.g.'5' to exit:") 
        # list contains functions in order of menu
        functions = [pr.proportion_of_rank,
                     sr.crew_memb_promotion_track,
                     hcs.num_crew_ship,
                     tv.port_visited_plot]
        if(m_input.isdigit()): # check if int
            if(int(m_input) == 5): # if 5 exit menu - increase int if add to menu
                break
            elif(int(m_input)>0 and int(m_input)<5): # makes sure in range
                functions[int(m_input)-1](db)  # calls chosen function

def main():
    """
    This function will make sure the databases are set up and once complete
    will send database collection address to the menu.
    
    args => None
    return => None
    """
    # connect to ship database
    client = MongoClient('mongodb://mah60:vz8n98g7stqz@nosql.dcs.aber.ac.uk/mah60')
    # create db collection locations for orginal and duplicate
    db  = client.mah60
    db_old = db.mah60
    db_dup = db.mah60_dup
    while True:  # ask if want to filter db
        lib1 = db_dup.find({}).count()
        lib2 = db_old.find({}).count()
        if(lib1 == lib2): # incase of crash
            print("Do you want to filter the database? y - yes, n - no ")
            print("If yes, please do not stop until finished")
            user_input = input("Enter answer: ")
            #user_input = 'n' 
            if(user_input.lower() == 'y'): # filter db
                f.create_filtered_db(db_old, db_dup)
                break
            elif(user_input.lower() == 'n'):
                break
            else:
                print('entered incorrect value')
        else: # if crash while filtering - continue filter
            f.create_filtered_db(db_old, db_dup)
            
    menu(db_dup)  # start menu loop


if __name__ == "__main__":
    main()

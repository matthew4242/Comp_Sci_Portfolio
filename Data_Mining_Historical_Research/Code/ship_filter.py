# -*- coding: utf-8 -*-
"""

@author: mah60
"""
from dateutil.parser import parse
import matplotlib
matplotlib.use('Agg')
import string as st


def create_filtered_db(db, db_dup):
    """
    Filters orginal database collection to the duplicate database collection.
    This is not to not modify the orginal values within the database, within
    this function the code with apply all generic filters towards the database.
    
    ags => db - db.col - the original database collection location
            db_dup - db.col - the duplication/filtered database collection
    return => None 
    """
    print("--------------------------------")
    print("please wait filtering..... this may take a moment \naround 2 miniutes")
    # make sure duplicate db is empty
    db_dup.delete_many({})
    # get records to be filtered
    sailor_db = db_dup.find({})

    sailor_db = db.find({})
    # main keys
    keys = ['port of registry', 'vessel name', 'mariners', 'official number']
    # keys in mariner
    sub_keys = ['place_of_birth', 'signed_with_mark', 'this_ship_joining_port',
                'name', 'additional_notes', 'this_ship_joining_date', 
                'last_ship_port', 'this_ship_capacity', 'last_ship_name',
                'this_ship_leaving_cause', 'last_ship_leaving_date', 
                'age', 'this_ship_leaving_port', 'home_address', 
                'this_ship_leaving_date', 'year_of_birth']

    # check for missing keys
#    for item in sailor_db:
#        for k in item.keys():
#            if(k not in keys):
#                print(k)
    for item in sailor_db:
        filtered_item = {}
        # check port of registry
        filtered_item[keys[0]] = string_filter(item[keys[0]], 1, 20)
        # check vessel name
        filtered_item[keys[1]] = string_filter(item[keys[1]], 1, 30)
        # check mariners values
        mariners = []
        num_values = ['age', 'year_of_birth']
        for marine in item[keys[2]]:
            details = {}
            for sk in sub_keys:
                # check if there is corrisponding key
                if(sk in marine.keys()):
                    key_value = marine[sk]
                    # filter sting first to remove unwanted symbols or letters/numbers
                    # check if appost to be date
                    if('date' in sk):
                        # remove unwanted symbols
                        key_value = remove_symbols(str(key_value).lower(), "[]$,.+&*,'",'')
                    elif(sk in num_values): # remove incorrect values from pure number keys
                        num = remove_symbols(str(key_value).lower(), st.ascii_letters,'')
                        num = remove_symbols(str(key_value).lower(), "[]$,.+&*,'",'')
                        if(str(key_value).isdigit()): # check if digit
                            key_value = num
                        else:
                            key_value = 'none'
                    elif(sk == sub_keys[7]):
                          key_value = remove_symbols(str(key_value), r"[]!(),.$-", '') 
                          key_value = remove_symbols(str(key_value), r"4567890", '') 
                    else: # remove incorrect values from string
                        key_value = string_filter(str(key_value).lower(), 1, 20)
                    # check if key is none or not - usually uses 'no info','blk'
                    null_values = ['no info', 'blk']
                    if(str(key_value).lower() in null_values or len(str(key_value)) == 0):
                        key_value = 'none'
                    # add to details list
                    if(key_value != 'none'):
                        details[sk] = key_value.lower()
                    else:
                        details[sk] = 'none'
                else: # if doesnt exist add as none
                    details[sk] = 'none' 
            mariners.append(details)   
        # add mariners to item
        filtered_item[keys[2]] = mariners
        # check official number
        if(str(item[keys[3]]).isdigit()):
            filtered_item[keys[3]] = item[keys[3]]
        else:
            filtered_item[keys[3]] = remove_symbols(str(item[keys[3]]), st.ascii_letters ,'')
        # add to filtered db list
        db_dup.insert_one(filtered_item)
    
    print("--------------------------------")
    print("filter complete!!")
    print("--------------------------------")
    #check if items in dup_db
#    sailor_db = db_dup.find({})
#    for item in sailor_db:
#        pprint(item)
    

def remove_symbols(string, symbols, convert):
    """
    Convert unwanted symbols.
    
    code from -> 
     https://www.journaldev.com/23674/python-remove-character-from-string 
     JournalDev - Pankaj
     05/05/2019
     
     args => string - string - sting to be modified
             symbols - string - characters to change
             convert - string - characters to change to
     return => string - modified string
    """
    string = string.translate({ord(i): convert for i in symbols})
    return string

def string_filter(string, min_len, max_len):
   """
   Filter string to remove unwanted symbols, numbers or spaces. Will make 
   sure that the code wont alter date values. AS well make sure the string
   is within a certain size
   
   args => string - string - string to be checked
           min_lin - integer - min length of the string
           max_len - integer - max length of the string
   return => string - string - string after being checked or modified
   """
   if(string != None):
       if(not is_date(string, fuzzy=False)): #  do not change date names
           # handling missing or tampered data
           string = remove_symbols(string, r"[]!(),.$", None) # remove []!
           string = remove_symbols(string, r"1234567890", None) #remove numbers and .
           string = list(string) # test 609
           if(len(string) >= min_len and len(string) <= max_len):
               if(string[0] == ' '):
                       del string[0]
   else:
       string = list('None')
   string = "".join(string)
   return string

def is_date(string, fuzzy=False):
    """
    https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
    Alex Riley - 16/08/2014 comment wrote date - read - 05/05/2019
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
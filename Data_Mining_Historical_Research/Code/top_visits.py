# -*- coding: utf-8 -*-
"""

@author: mah60
"""

from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def port_visited_plot(db):
    """
    Calculates the amounts of ships that vists x port. This will be done
    for each port and plotted. This will be plotted and saved as name.png.
    
    ags => db - db.col - the database collection
    return => None
    """
    # search for unique ships leaving and entering ports
    ports_visits = db.aggregate([{"$unwind": "$mariners"},
                           {"$group": { "_id": {
            'joining_port': "$mariners.this_ship_joining_port",
            'leaving_port': "$mariners.this_ship_leaving_port",
            'vessel name': "$vessel name",
            'official number': "$official number"
            }}}])
    # calculate totals for visits for each port
    total_port_visits = {}
    for pv in ports_visits:
        for ship in pv:
            # add up joining ports visits
            if(pv[ship]['joining_port'] in total_port_visits.keys()):
                total_port_visits[pv[ship]['joining_port']] = total_port_visits[pv[ship]['joining_port']] + 1
            else:
                total_port_visits[pv[ship]['joining_port']] = 1
            # add up leaving ports visits
            if(pv[ship]['leaving_port'] in total_port_visits.keys()):
                total_port_visits[pv[ship]['leaving_port']] = total_port_visits[pv[ship]['leaving_port']] + 1
            else:
                total_port_visits[pv[ship]['leaving_port']] = 1
            
    # find top 10 values which are not aberystwth
    # create array with id and value
    total_values = [] # [id, total_value]
    total_names = [] # [id, total_name]
    for i, total_v in enumerate(total_port_visits.keys()):
        if(total_v != 'aberystwyth' and total_v != 'none'): # remove null values
                                                            # and aberystwyth
            total_values.append([i, total_port_visits[total_v]])
            total_names.append([i, total_v])
            
    top = 10 # top value
    ordered_total_values = find_top_visits(total_values, top)
    
    # now ordered reconnect values and plot
    yaxis = []
    lab = []
    
    for otv in ordered_total_values:
        # add top value
        done = False # when false - havent found name
        for names in total_names: 
            if(not done):
                if(otv[0] == names[0]): # then add x,y values
                    lab.append(names[1])
                    yaxis.append(otv[1])
                    done = True
    ind = np.arange(len(lab))
    # variables made time to plt
    plt.barh(ind, yaxis)
    plt.yticks(ind, lab, rotation=50, fontsize=7)
    plt.xlabel("Number of visits")
    plt.ylabel("Port Name")
    plt.title("Top {} Ports Visited \n(That are not Aberystwyth)".format(top))
    for x, y in zip(yaxis, ind):
        plt.text(x, y, str(x), rotation=330, fontsize=7)
    str_file = "top_port_visits.png"
    if os.path.isfile(str_file):
       os.remove(str_file)   # delete file; if exsits 
    plt.savefig(str_file, dpi=gcf().dpi)
    plt.show()
    plt.close()
    
    

def find_top_visits(totals, top):
    """
    Will find top areas visited, this will be done by sorting a list of
    integers(the totals). This will return them in order and up to a max of 
    top.
    
    args => totals - list[list] - [[ID, Total]]
            top - integer - number for top value
    return => new_totals - list[list] - [[ordered_ID, Total]]
    """
    # create date array
    total_array = []
    for d in totals:
        total_array.append(d[1])
    total_array.sort(reverse=True)
    # connect id
    new_totals = []
    used_id = [] # make sure no replica ids produced
    # match totals with IDs 
    for ta in total_array:
        if(len(new_totals) != top):
            for t in totals:
                if(ta == t[1]):
                    # make sure id not already taken
                    if(t[0] not in used_id):
                        new_totals.append([t[0], t[1]])
                        used_id.append(t[0])
    return new_totals
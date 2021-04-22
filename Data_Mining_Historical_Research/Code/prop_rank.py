# -*- coding: utf-8 -*-
"""

@author: Mhowa
"""
from matplotlib.pyplot import *

import matplotlib.pyplot as plt
import numpy as np
import os
import time


def proportion_of_rank(db):
    """
    This method will gather data about the individual ranks on each ship.
    Then plot a graph that will display the total for each rank and 
    will be saved to the current file location as a name.png.
    
    ags => db - db.col - the database collection
    return => None
    """
    ship_crew = db.aggregate([
		{"$project": {"_id": False, "mariners.this_ship_capacity": True}}])
    # get totals for each crew ranks
    # classify the data
    correct_value = [ # [correct value, alternatives in db]]
            ["second ", "nd", "2nd"]  # need to add more classifications/translates
            ]
    ship_ranks = ['master', 'chief officer', ' chief mate', 'second officer',
          'second mate', 'third officer', 'third mate', 'cadet',
          'ab', 'os', 'boatswain', 'chief engineer',
          'first engineer', 'second engineer', 'third engineer',
          'second officer', 'third officer', 'deck cadet', 
          'electrical officer', 'oilerwiper seaman', 'pumpman',
          'electrician', 'engine cadet', 'fitter', 'motorman']
    rank_total = {} # to gather rank totals
    for item in ship_crew:
        for sc in item['mariners']:
            if(sc['this_ship_capacity'] != 'none'):
                for cv in correct_value: # classifying data
                    if(sc['this_ship_capacity'][0:3] in cv):
                        x = 'found'                  
                # add to totals
                if(sc['this_ship_capacity'] in rank_total.keys()):
                    rank_total[sc['this_ship_capacity']] = rank_total[sc['this_ship_capacity']] + 1
                else:
                    rank_total[sc['this_ship_capacity']] = 1

    # calculate total number for proportions
    total = 0
    for r in rank_total:
          total = rank_total[r] + total
    # remove ranks of totals less than x
    remove_rank = []
    for rank in rank_total:
        if rank not in ship_ranks:
            if(rank_total[rank] <= 30000):
                remove_rank.append(rank)
    # delete from rank totals
    for rank in remove_rank:
        del rank_total[rank]
        
    # create variables for plot
    indexs = np.arange(len(rank_total))
    heights = []
    labels = []
    for rank in rank_total:
        labels.append(rank)
        heights.append(rank_total[rank]/total*100)
    # plot graph
    plt.barh(indexs, heights)
    #print(indexs)
    plt.yticks(indexs, labels, rotation=50, fontsize=5)
    plt.xlabel("Proportions (Percentage %)")
    plt.ylabel("Rank")
    plt.title("Proportions of individual Ranks")
    # plot values at end of graphs
    for x, y in zip(heights, indexs):
        plt.text(x, y, str(round(x,3)), rotation=320, fontsize=5)
    str_file = "proportions_rank.png"
    if os.path.isfile(str_file):
       os.remove(str_file)   # delete file; if exsits 
    plt.savefig(str_file, dpi=gcf().dpi)
    plt.show()
    plt.close()

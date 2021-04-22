# -*- coding: utf-8 -*-
"""

@author: mah60
"""

from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import time
import os

def num_crew_ship(db):
    """
    This method will create the visualisation for the number of crew on each
    ship. This results will be a histogram and will be saved to the current
    file location as a name.png.
    
    ags => db - db.col - the database collection
    return => None
    """
    # find crew size for ships
    results = db.aggregate([{"$project": {
            "_id": False,
            "crew_size": {"$size": '$mariners'},
            "vessel name": True,
            "official number": True
                }}])
    
    #match_ship = {}
    crew_on_ship = []
    for size in results:
        crew_on_ship.append(size['crew_size'])

    # plot histograms
    plt.hist(crew_on_ship, bins=60)
    plt.ylabel('frequency')
    plt.xlabel('number of crew on each ship')
    plt.title('Histogram of number of crew on each ship')
    str_file = "hist_crew_ship.png"
    if os.path.isfile(str_file): 
       os.remove(str_file)   # delete file; if exsits 
    plt.savefig(str_file, dpi=gcf().dpi)
    plt.show()
    plt.close()
    
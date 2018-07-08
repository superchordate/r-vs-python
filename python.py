# Set up workspace.
    
# Necessary packages.
import pandas as pd
import pandas
import numpy as np
import time
import math
from os import chdir
from dfply import *

chdir('F://0-active/r-v-python'  )

# Read the file, timing the operation.
start_time = time.clock()
d0 = pandas.read_csv( 'data.csv' )
print( 'Read (s) : ' + str( time.clock() - start_time ) )

# Convert usertype to category to make it equivalent to factor in R.
d1 = d0.copy()
start_time = time.clock()
d1.usertype = d1.usertype.astype('category')
print( 'Convert usertype to category : ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )


# Filter to Subscriber.
start_time = time.clock()
d1 = d0 >> mask( X.usertype == 'Subscriber' )
print( 'Filter : ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )


# Haversine distance of trip.
start_time = time.clock()
d1 = d1 >> mutate(
        
    # Stage radian lat/lng.        
    slat = X.latitude_start * math.pi / 180,
    elat = X.latitude_end * math.pi / 180,
    slng = X.longitude_start * math.pi / 180,
    elng = X.longitude_end * math.pi / 180
    
)

# np functions don't work with X, you must use d1.
d1 = d1 >> mutate(

    # Calculate great-circle distance. See https://www.r-bloggers.com/great-circle-distance-calculations-in-r/.
    tripdistance = 6371 * np.arccos(
      np.sin( d1.slat ) * np.sin( d1.elat ) 
      + np.cos( d1.slat ) * np.cos( d1.elat ) * np.cos( d1.elng - d1.slng ) )
                
)                
print( 'Great-cirlce distance : ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )


# Get mean trip distance by the starting station.
start_time = time.clock()
d1 = d1 >> group_by( X.from_station_name ) >> summarize( 
    meantrip = X.tripdistance.mean() 
)
print( 'Group and mean : ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )


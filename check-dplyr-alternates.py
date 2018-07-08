# Set up workspace.
    
# Necessary packages.
import pandas as pd
import pandas
import numpy as np
import time
import math
from os import chdir

chdir('F://0-active/r-v-python'  )

# Read the data.
d0 = pandas.read_csv( 'data.csv' )

# Test methods:

# base pyton.
start_time = time.clock()
d0 = d0.assign( slat = d0.latitude_start * math.pi / 180 )
d0 = d0.assign( elat = d0.latitude_end * math.pi / 180 )
d0 = d0.assign( slng = d0.longitude_start * math.pi / 180 )
d0 = d0.assign( elng = d0.longitude_end * math.pi / 180 )            
print( 'Base python: ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )


# pandas_ply
from pandas_ply import install_ply, X, sym_call
install_ply(pd)

start_time = time.clock()
dt = d0.ply_where( X.usertype == 'Subscriber' ).ply_select(
    slat = X.latitude_start * math.pi / 180,
    elat = X.latitude_end * math.pi / 180,
    slng = X.longitude_start * math.pi / 180,
    elng = X.longitude_end * math.pi / 180        
)
print( 'pandas_ply: ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )

# dplython
import pandas
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
    sample_frac, head, arrange, mutate, group_by, summarize, DelayFunction) 

start_time = time.clock()
dt = DplyFrame(d0) >> sift( X.usertype == 'Subscirber' ) >> mutate(
    slat = X.latitude_start * math.pi / 180,
    elat = X.latitude_end * math.pi / 180,
    slng = X.longitude_start * math.pi / 180,
    elng = X.longitude_end * math.pi / 180
)
print( 'dplython: ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )

# dfply
from dfply import *
import pandas as pd

start_time = time.clock()
dt =d0 >> mask( X.usertype == 'Subscirber' ) >> mutate(
    slat = X.latitude_start * math.pi / 180,
    elat = X.latitude_end * math.pi / 180,
    slng = X.longitude_start * math.pi / 180,
    elng = X.longitude_end * math.pi / 180
)
print( 'dfply: ' + str( round( time.clock() - start_time, 2 ) ) + ' seconds.' )



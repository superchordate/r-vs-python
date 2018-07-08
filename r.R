# Set up workspace.

  # Packages I'll use.
  require(dplyr)
  require(magrittr)
  require(data.table)
  require(ggplot2)
  
  # Clear any variables.
  rm(list=ls(all=TRUE))
  
  # Set default path location to the current file.
  setwd( dirname( rstudioapi::getActiveDocumentContext()$path ) ) # set directory to location of file.
  
  # Read the file, timing the operation.
  d0 = fread( '../data.csv' )
  
# Filter to Subscriber.
  
  system.time({
    d1 = d0 %>% filter( usertype == 'Subscriber' )
  })
  
# Distance of trip, using dplyr.
  
  system.time({
    
    d1 %<>% mutate(
      
      # stage radian lat/long.
      slat = latitude_start * pi / 180,
      slng = longitude_start * pi / 180,
      elat = latitude_end * pi / 180,
      elng = longitude_end * pi / 180,
      
      # great-circle distance. See https://www.r-bloggers.com/great-circle-distance-calculations-in-r/.
      trip.distance = 6371 * acos(
        sin( slat ) * sin( elat ) 
        + cos( slat ) * cos( elat ) * cos( elng - slng ) )
      
    )
    
    d1 %>% select( slat, slng, elat, elng, trip.distance ) %>% head()
    
  })

# Get mean trip distance by the starting station.
  
  system.time({
    
    d2 = d1 %>% group_by( from_station_name ) %>% 
      summarize( mean.trip = mean(trip.distance) )
    
  })

# Plot.
  
  system.time({
    
    p1 = d2 %>% top_n( 15, mean.trip ) %>%
      ggplot( aes( x = from_station_name, y = mean.trip) ) + 
      geom_bar( stat = 'identity' ) + 
      theme( axis.text.x = element_text( angle = 90, hjust = 1 ) )
    
  })
  
  p1
  
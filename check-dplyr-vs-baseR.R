# Set up workspace.

  # Packages I'll use.
  require(dplyr)
  require(data.table)
  
  # Clear any variables.
  rm(list=ls(all=TRUE))
  
  # Set default path location to the current file.
  setwd( dirname( rstudioapi::getActiveDocumentContext()$path ) ) # set directory to location of file.
  
  # Read the file, timing the operation.
  d1 = fread( 'data.csv' )

# Base R.
  
  system.time({
    
    d1$slat = d1$latitude_start*pi/180
    d1$slng = d1$longitude_start*pi/180
    d1$elat = d1$latitude_end*pi/180
    d1$elng = d1$longitude_end*pi/180
    
  })
  
  
# dplyr.
  
  system.time({
    
    d1 %<>% mutate(
      
      # stage radian lat/long.
      slat = latitude_start*pi/180,
      slng = longitude_start*pi/180,
      elat = latitude_end*pi/180,
      elng = longitude_end*pi/180
    )
    
  })
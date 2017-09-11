# Industry_Briefings
Codes used to produce the datasets behind the indsutry briefing visuals

To perform the brand to brand analysis, your input file will need to be of the following format:  
`fan_id, star_id, timestamp`  
`20582087,34892616,2015-01-14 00:00:00`  
`20582087,215794846,2015-06-14 23:00:00` 
  
To get this file, you will need to pull the star-date metrics from a fan file using the tool server: http://192.168.1.201:8888/notebooks/Hive%20Demos.ipynb#  

If you havent used it before, make a copy of the notebook, under your name.    

If you have used the tool server to pull your fan, star, time file, the timestamp will be in unix time, and will be headed 'datestamp'  

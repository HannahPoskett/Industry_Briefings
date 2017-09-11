# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:55:34 2017
@author: Hannah Poskett
"""

import pandas as pd
#########################################
#RUN FAN BRAND FLOWS OVER TIME.PY
#########################################
# Find flow of fans between stars over time

#parameters
all_fan_stars = r'Z:\lookgood_feelgood\influencer_flows\lgfg_stars_followed.csv'
tagged_stars = r'Z:\lookgood_feelgood\influencer_flows\lgfg_stars_followed.csv'
star1 = 'EsteeLauder'
star2 = 'KendallJenner'
star3 = 'victoriabeckham'
star4 = 'Fendi'
star5 = 'GiGiHadid'
output_loc = r'Z:\lookgood_feelgood\influencer_flows\estee_lauder_flow_new.csv'

all_fan_stars['timestamp'] = pd.to_datetime(all_fan_stars.datestamp, unit='s')
all_fan_stars['timestamp'] = all_fan_stars['timestamp'].astype('str')

fan_following = all_fan_stars.merge(tagged_stars, left_on = 'star_id', right_on = 'Network_Id', how = 'inner')
fan_following = fan_following[['fan_id','star_id', 'timestamp', 'Account_Username']]
fan_following = fan_following[fan_following.Account_Username.notnull()]
fan_following = fan_following[fan_following.timestamp.notnull()]
fan_following['Ctr'] = 1

### Select which 5 Brands or Influencers you want to look at
# CHANGE THE ACCOUNT USERNAMES TO BE THE BRANDS OR INFLUENCERS YOU WANT
a = fan_following[fan_following['Account_Username'] == star1]
b = fan_following[fan_following['Account_Username'] == star2]
c = fan_following[fan_following['Account_Username'] == star3]
d = fan_following[fan_following['Account_Username'] == star4]
e = fan_following[fan_following['Account_Username'] == star5]
fan_following_brands = pd.concat([a,b,c,d,e])

fan_following_brands[['date','time']] = fan_following_brands['timestamp'].str.split(" ", expand=True)
fan_following_brands = fan_following_brands[['fan_id','date','Account_Username','Ctr']]
fan_following_brands = fan_following_brands.sort_values(['fan_id','date'], ascending = True)

min_date = fan_following_brands.groupby('fan_id')['date'].min().reset_index()
min_brand_date = min_date.merge(fan_following_brands, on = ['fan_id','date'], how = 'inner')
min_brand_date = min_brand_date.groupby(['date','Account_Username']).size().reset_index()
min_brand_date.rename(columns = {0:'Ctr'}, inplace = True)
min_brand_date['Cumulative'] = min_brand_date.groupby(['Account_Username'])['Ctr'].cumsum()

min_brand_date_match = min_brand_date.merge(min_brand_date, on = 'date', how = 'inner')
min_brand_date_match.rename(columns = {'date':'date_x'}, inplace = True)

fan_following_match = fan_following_brands.merge(fan_following_brands, on = 'fan_id', how = 'inner')
fan_following_match = fan_following_match.drop_duplicates()
fan_following_match[['date_x','date_y']] = fan_following_match[['date_x','date_y']].astype('datetime64[ns]')
fan_following_match['Moved'] = (fan_following_match.date_y>fan_following_match.date_x).astype(int)

moved = fan_following_match.groupby(['date_x','Account_Username_x','Account_Username_y'])['Moved'].sum().reset_index()

min_brand_date_match['date_x'] = min_brand_date_match.date_x.astype('datetime64[ns]')

date_brand_moved = min_brand_date_match.merge(moved, on = ['date_x','Account_Username_x','Account_Username_y'], how = 'inner')
date_brand_moved_rename = date_brand_moved.copy()

date_brand_moved = min_brand_date_match.merge(moved, on = ['date_x','Account_Username_x','Account_Username_y'], how = 'inner')
date_brand_moved_rename = date_brand_moved.copy()
date_brand_moved_rename.rename(columns = {'Account_Username_x':'Account_Username_y','Account_Username_y':'Account_Username_x'}, inplace = True)
date_brand_moved_rename = date_brand_moved_rename.merge(moved, on = ['date_x','Account_Username_x','Account_Username_y'], how = 'inner')
date_brand_moved_rename['net_move'] = date_brand_moved_rename.Moved_y - date_brand_moved_rename.Moved_x

Final_brand_flow = date_brand_moved_rename.copy()
Final_brand_flow = Final_brand_flow[['date_x','Account_Username_y','Cumulative_x','Account_Username_x','Cumulative_y','Moved_x','Moved_y','net_move']]
Final_brand_flow.rename(columns = {'date_x':'Timestamp','Account_Username_y':'Brand1','Cumulative_x':'Fan_Count1','Account_Username_x':'Brand2','Cumulative_y':'Fan_Count2','Moved_x':'Moved_In','Moved_y':'Moved_Out','net_move':'Net_Move'}, inplace = True)
Final_brand_flow = Final_brand_flow.sort_values('Timestamp', ascending = True)
output = Final_brand_flow.copy()
output = output[['Timestamp','Brand1','Brand2','Fan_Count1','Fan_Count2','Moved_Out']]
output.to_csv(output_loc, index = None)

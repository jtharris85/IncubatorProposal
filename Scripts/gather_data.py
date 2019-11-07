import pandas as pd
import numpy as np
import glob

#Create GBD Original
all_files_gbd = glob.glob('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\GBD_All\\*.csv')

all_gbd = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f)
    all_gbd = all_gbd.append(df, ignore_index = True)

all_deaths = all_gbd.loc[all_gbd['measure_id'] == 1]
all_daly = all_gbd.loc[all_gbd['measure_id'] == 2]

death_count = (all_deaths.loc[all_deaths['metric_id'] == 1]).groupby(['cause_name','year', 'location_name']).sum().sort_values(['val'], ascending = False)[['val']]
daly_count = (all_daly.loc[all_daly['metric_id'] == 2]).groupby(['cause_name','year']).sum().sort_values(['val'], ascending = False)

#Create RePORTER Master
all_files_reporter = glob.glob('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\RePORTER\\*.csv')

all_reporter = pd.DataFrame()
for r in all_files_reporter:
    df = pd.read_csv(r, low_memory = False, encoding = 'latin-1')
    all_reporter = all_reporter.append(df, ignore_index = True)

#Create Cause Hierarchy
cause_hierarchy = pd.read_excel('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\GBD_2017_heirarchies\\Cause_Hierarchy.xlsx', sheet_name='Cause Hierarchy Table', header=0, index_col=False, keep_default_na=True)
trim_cause_hierarchy = cause_hierarchy.drop(columns = ['Unnamed: 0', 'Cat A - Short', 'Cat B - Short', 'Cat C - Short', 'Cat D - Short', 'Cat D - Med'])

#Add Cause to GBD
gbd_cause = all_gbd.join(trim_cause_hierarchy.set_index('Cat D - Full'), on = 'cause_name')
gbd_cause.drop(columns = ['Cat A - Med', 'Cat B - Med', 'Cat C - Med', 'cause_id'], inplace = True)

#Create GBD Master with all Death/DALY counts
join_deaths = gbd_cause.loc[gbd_cause['measure_id'] == 1]
join_daly = gbd_cause.loc[gbd_cause['measure_id'] == 2]
join_death_count = (join_deaths.loc[join_deaths['metric_id'] == 1]).groupby(['location_name','year','Cat A - Full','Cat B - Full','cause_name']).sum().sort_values(['location_name','year','val'], ascending = False)[['val']]
join_daly_count = (join_daly.loc[join_daly['metric_id'] == 2]).groupby(['location_name','year', 'Cat A - Full', 'Cat B - Full', 'cause_name']).sum().sort_values(['location_name', 'year', 'val'], ascending = False)[['val']]
join_death_count.rename(columns = {'val':'Deaths'}, inplace = True)
join_daly_count.rename(columns = {'val':'DALYs'}, inplace = True)
death_dalys = pd.concat([join_death_count, join_daly_count], axis = 1).reindex(join_death_count.index)
death_dalys['DeathRank'] = death_dalys['Deaths'].groupby(['location_name', 'year']).rank(ascending = False)
death_dalys['DALYsRank'] = death_dalys['DALYs'].groupby(['location_name', 'year']).rank(ascending = False)

death = gbd_cause['measure_id'] == 1
dalys = gbd_cause['measure_id'] == 2
prevalence = gbd_cause['measure_id'] == 5
incidence = gbd_cause['measure_id'] == 6
counts = gbd_cause['metric_id'] == 1
percent = gbd_cause['metric_id'] == 2
rate = gbd_cause['metric_id'] == 3
states = gbd_cause['location_name'] == 'United States'
world = gbd_cause['location_name'] =='Global'

gbd_cause_deaths_US = gbd_cause[death & counts & states].rename(columns={'val':'DeathsUS','upper':'DeathsUpperUS','lower':'DeathsLowerUS'})
gbd_cause_dalys_US = gbd_cause[dalys & counts & states].rename(columns={'val':'DALYsUS','upper':'DALYsUpperUS','lower':'DALYsLowerUS'})
gbd_cause_prevalence_US = gbd_cause[prevalence & counts & states].rename(columns={'val':'PrevalenceUS','upper':'PrevUpperUS','lower':'PrevLowerUS'})
gbd_cause_incidence_US = gbd_cause[incidence & counts & states].rename(columns={'val':'IncidenceUS','upper':'IncUpperUS','lower':'IncLowerUS'})
gbd_cause_deaths_world = gbd_cause[death & counts & world].rename(columns={'val':'DeathsWorld','upper':'DeathsUpperWorld','lower':'DeathsLowerWorld'})
gbd_cause_dalys_world = gbd_cause[dalys & counts & world].rename(columns={'val':'DALYsWorld','upper':'DALYsUpperWorld','lower':'DALYsLowerWorld'})
gbd_cause_prevalence_world = gbd_cause[prevalence & counts & world].rename(columns={'val':'PrevalenceWorld','upper':'PrevUpperWorld','lower':'PrevLowerWorld'})
gbd_cause_incidence_world = gbd_cause[incidence & counts & world].rename(columns={'val':'IncidenceWorld','upper':'IncUpperWorld','lower':'IncLowerWorld'})

gbd_cause_deaths_US.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_US.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_US.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_US.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_deaths_world.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_world.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_world.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_world.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)

gbd_cause_deaths_US_perc = gbd_cause[death & percent & states].rename(columns={'val':'Death%US','upper':'DeathsUpper%US','lower':'DeathsLower%US'})
gbd_cause_dalys_US_perc = gbd_cause[dalys & percent & states].rename(columns={'val':'DALYs%US','upper':'DALYsUpper%US','lower':'DALYsLower%US'})
gbd_cause_prevalence_US_perc = gbd_cause[prevalence & percent & states].rename(columns={'val':'Prevalence%US','upper':'PrevUpper%US','lower':'PrevLower%US'})
gbd_cause_incidence_US_perc = gbd_cause[incidence & percent & states].rename(columns={'val':'Incidence%US','upper':'IncUpper%US','lower':'IncLower%US'})
gbd_cause_deaths_world_perc = gbd_cause[death & percent & world].rename(columns={'val':'Deaths%World','upper':'DeathsUpper%World','lower':'DeathsLower%World'})
gbd_cause_dalys_world_perc = gbd_cause[dalys & percent & world].rename(columns={'val':'DALYs%World','upper':'DALYsUpper%World','lower':'DALYsLower%World'})
gbd_cause_prevalence_world_perc = gbd_cause[prevalence & percent & world].rename(columns={'val':'Prevalence%World','upper':'PrevUpper%World','lower':'PrevLower%World'})
gbd_cause_incidence_world_perc = gbd_cause[incidence & percent & world].rename(columns={'val':'Incidence%World','upper':'IncUpper%World','lower':'IncLower%World'})
gbd_cause_deaths_US_rate = gbd_cause[death & rate & states].rename(columns={'val':'DeathsRateUS','upper':'DeathsRateUpperUS','lower':'DeathsRateLowerUS'})
gbd_cause_dalys_US_rate = gbd_cause[dalys & rate & states].rename(columns={'val':'DALYsRateUS','upper':'DALYsRateUpperUS','lower':'DALYsRateLowerUS'})
gbd_cause_prevalence_US_rate = gbd_cause[prevalence & rate & states].rename(columns={'val':'PrevalenceRateUS','upper':'PrevRateUpperUS','lower':'PrevRateLowerUS'})
gbd_cause_incidence_US_rate = gbd_cause[incidence & rate & states].rename(columns={'val':'IncidenceRateUS','upper':'IncRateUpperUS','lower':'IncRateLowerUS'})
gbd_cause_deaths_world_rate = gbd_cause[death & rate & world].rename(columns={'val':'DeathsRateWorld','upper':'DeathsRateUpperWorld','lower':'DeathsRateLowerWorld'})
gbd_cause_dalys_world_rate = gbd_cause[dalys & rate & world].rename(columns={'val':'DALYsRateWorld','upper':'DALYsRateUpperWorld','lower':'DALYsRateLowerWorld'})
gbd_cause_prevalence_world_rate = gbd_cause[prevalence & rate & world].rename(columns={'val':'PrevalenceRateWorld','upper':'PrevRateUpperWorld','lower':'PrevRateLowerWorld'})
gbd_cause_incidence_world_rate = gbd_cause[incidence & rate & world].rename(columns={'val':'IncidenceRateWorld','upper':'IncRateUpperWorld','lower':'IncRateLowerWorld'})

gbd_cause_deaths_US_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_US_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_US_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_US_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_deaths_world_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_world_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_world_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_world_perc.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_deaths_US_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_US_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_US_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_US_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_deaths_world_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_dalys_world_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_prevalence_world_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)
gbd_cause_incidence_world_rate.drop(columns=['measure_id','measure_name','location_id','location_name','metric_id','metric_name'], inplace=True)

list_gbd_cause_df = [gbd_cause_deaths_US,
                     gbd_cause_dalys_US,
                     gbd_cause_prevalence_US,
                     gbd_cause_incidence_US,
                     gbd_cause_deaths_world,
                     gbd_cause_dalys_world,
                     gbd_cause_prevalence_world,
                     gbd_cause_incidence_world,
                     gbd_cause_deaths_US_perc,
                     gbd_cause_dalys_US_perc,
                     gbd_cause_prevalence_US_perc,
                     gbd_cause_incidence_US_perc,
                     gbd_cause_deaths_world_perc,
                     gbd_cause_dalys_world_perc,
                     gbd_cause_prevalence_world_perc,
                     gbd_cause_incidence_world_perc,
                     gbd_cause_deaths_US_rate,
                     gbd_cause_dalys_US_rate,
                     gbd_cause_prevalence_US_rate,
                     gbd_cause_incidence_US_rate,
                     gbd_cause_deaths_world_rate,
                     gbd_cause_dalys_world_rate,
                     gbd_cause_prevalence_world_rate,
                     gbd_cause_incidence_world_rate]

for df in list_gbd_cause_df:
    df.drop(columns=['sex_id','age_id'], inplace=True)
    df.rename(columns={'sex_name':'Sex','age_name':'Age','cause_name':'Cause','Cat B - Full':'CauseClass','Cat A - Full':'CauseType','Cat C - Full':'CauseFamily'}, inplace=True)

for df in list_gbd_cause_df:
    df.set_index(['Sex', 'Age', 'year', 'CauseType', 'CauseClass', 'CauseFamily', 'Cause'], inplace = True)

gbd_cause_index = ['Sex', 'Age', 'year', 'CauseType', 'CauseClass', 'CauseFamily', 'Cause']

for df in list_gbd_cause_df:
    for column in list(df):
        list_gbd_cause_df[23][column] = df[column]

gbd_cause_master = list_gbd_cause_df[23]

gbd_cause_master.reset_index(inplace = True)

gbd_cause_master.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_cause_master.csv')

#Start by running data_loading.py to produce:
#reporter_cause_year
#gbd_cause_master

#Filters
all_ages = gbd_cause_master['Age'] =='All Ages'
standard_ages = gbd_cause_master['Age'] == 'Age-standardized'
year_2000 = (gbd_cause_master['year'] >= 2000)

#Restrict to year 2000+ and Group to match RePORTER
reporter_cause_update = reporter_cause_year.rename({"Unnamed: 0":"a"}, axis="columns").drop(columns = 'a').groupby(['year','CauseType','CauseClass','CauseFamily']).sum()
total_cause = gbd_cause_master[year_2000].rename({"Unnamed: 0":"a"}, axis="columns").drop(columns = 'a').groupby(['year','CauseType','CauseClass','CauseFamily']).sum()
gbd_reporter_pretrim = total_cause.join(reporter_cause_update, on = ('year','CauseType','CauseClass','CauseFamily'))
#Restrict to causes with actual reported DALYs to remove negatives
dalys_cause = (gbd_reporter_pretrim['DALYsUS'] >= 0) | (gbd_reporter_pretrim['DALYsWorld'] >= 0)
gbd_reporter_all = gbd_reporter_pretrim[dalys_cause].fillna(0)
gbd_reporter_all.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_all.csv')
#Define new DF of various groupings
gbd_reporter_class = gbd_reporter_all.groupby(['year','CauseType','CauseClass']).sum()
gbd_reporter_type = gbd_reporter_all.groupby(['year','CauseType']).sum()
gbd_reporter_total = gbd_reporter_all.reset_index().groupby(['CauseFamily']).sum()

#Add ranking columns
rank_dict = {'DeathRankUS':'DeathsUS',
             'DeathRankWorld':'DeathsWorld',
             'DALYRankUS':'DALYsUS',
             'DALYRankWorld':'DALYsWorld',
             'SpendRank':'TOTAL_COST',
             'DeathUS_SpR_Rank':'DeathUS_SpR',
             'DeathWorld_SpR_Rank':'DeathWorld_SpR',
             'DALYsUS_SpR_Rank':'DALYsUS_SpR',
             'DALYsWorld_SpR_Rank':'DALYsWorld_SpR'}

rank_differences = {'Spend-DeathUS':'DeathRankUS',
                   'Spend-DeathWorld':'DeathRankWorld',
                   'Spend-DALYsUS':'DALYRankUS',
                   'Spend-DALYsWorld':'DALYRankWorld'}

spend_ratio = {'DeathUS_SpR':'DeathsUS',
                'DeathWorld_SpR':'DeathsWorld',
                'DALYsUS_SpR':'DALYsUS',
                'DALYsWorld_SpR':'DALYsWorld'}

gbd_reporter_dataframes = [gbd_reporter_all,
                          gbd_reporter_class,
                          gbd_reporter_type,
                          gbd_reporter_total]

def get_ratio(df,ratio_dict):
    for ratio in ratio_dict:
        df[ratio] = df['TOTAL_COST'] / df[ratio_dict[ratio]]
        df.replace([np.inf, -np.inf], 0, inplace = True)

def get_ranking(df,group_columns,rank_columns):
    for rank in rank_columns:
        if group_columns == 'None':
            df[rank] = df[rank_columns[rank]].rank(ascending = False)
        else:
            df[rank] = df[rank_columns[rank]].groupby([group_columns]).rank(ascending = False)

def get_diff(df,diff_dict):
    for diff in diff_dict:
        df[diff] = df[diff_dict[diff]] - df['SpendRank']

for df in gbd_reporter_dataframes:
    get_ratio(df, spend_ratio)
    if df is gbd_reporter_total:
        group = 'None'
    else:
        group = 'year'
    get_ranking(df, group, rank_dict)
    get_diff(df, rank_differences)

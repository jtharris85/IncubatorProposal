#Build up rankings categories for full characterizations

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

#Save all DFs
gbd_reporter_all.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_all.csv')
gbd_reporter_class.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_class.csv')
gbd_reporter_type.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_type.csv')
gbd_reporter_total.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_total.csv')

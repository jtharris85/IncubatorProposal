import pandas as pd

#Load data for further processing
df_dict = {'gbd_cause_master':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_cause_master.csv',
#'all_reporter':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\all_reporter.csv',
'reporter_cause_year':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\reporter_cause_year.csv'}
#'gbd_reporter_all':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_all.csv',
#'gbd_reporter_class':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_class.csv',
#'gbd_reporter_type':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_type.csv',
#'gbd_reporter_total':'C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\gbd_reporter_total.csv'}

df_list = []
for df in df_dict:
    df_list[df] = pd.read_csv(df_dict[df])

gbd_cause_master = df_dict['gbd_cause_master']
#all_reporter = df_dict['all_reporter']
reporter_cause_year = df_dict['reporter_cause_year']
#gbd_reporter_all = df_dict['gbd_reporter_all']
#gbd_reporter_class = df_dict['gbd_reporter_class']
#gbd_reporter_type = df_dict['gbd_reporter_type']
#gbd_reporter_total = df_dict['gbd_reporter_total']

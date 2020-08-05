import pandas as pd
from collections import defaultdict
from Constants import *


def import_covid():
    col_types = defaultdict(int)
    col_types['continent'] = 'str'
    col_types['location'] = 'str'
    covid = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv", usecols=cols, dtype=col_types, parse_dates=['date'], index_col='date')
    covid = covid[covid.continent=='Europe']
    covid = covid[covid.continent=='Europe'].drop(['continent'], axis=1)
    return covid

def get_latest_available_date(country_df):
    mask_nci = country_df[['NCI']].notna().values
    latest_avail_nci = country_df.loc[mask_nci, ['NCI']].iloc[-1].name

    mask_ppt = country_df[['PPT']].notna().values
    latest_avail_ppt = country_df.loc[mask_ppt, ['PPT']].iloc[-1].name
    return latest_avail_nci, latest_avail_ppt

def assess_norwegian_metrics(covid, country_name):
    data = covid[covid.location == country_name].drop(['location'], axis=1)
    if country_name == 'Italy':
        data[['new_cases', 'new_cases_per_million']] = data[['new_cases', 'new_cases_per_million']].shift(-1)
    data['NCI'] = data['new_cases_per_million'].rolling(DT_int).sum()/10
    data['PPT'] = (data['new_cases'].divide(data['new_tests'])*100).rolling(DT_int).mean()
    latest_date_nci, latest_date_ppt = get_latest_available_date(data)

    return data, latest_date_nci, latest_date_ppt

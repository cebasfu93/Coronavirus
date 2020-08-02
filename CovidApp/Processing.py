import pandas as pd
from collections import defaultdict
from Constants import *


def import_covid():
    cols = ['date', 'new_cases_per_million', 'new_cases', 'new_tests', 'population', 'continent', 'location']
    col_types = defaultdict(int)
    col_types['continent'] = 'str'
    col_types['location'] = 'str'
    covid = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv", usecols=cols, dtype=col_types, parse_dates=['date'], index_col='date')
    covid = covid[covid.continent=='Europe']
    covid = covid[covid.continent=='Europe'].drop(['continent'], axis=1)
    return covid

def get_latest_available_date(country_df):
    mask_completeness = country_df.isna().sum(axis=1)==0
    latest_avail = country_df.loc[mask_completeness].iloc[-1].name
    return latest_avail

def assess_norwegian_metrics(covid, country_name):
    data = covid[covid.location == country_name].drop(['location'], axis=1)
    if country_name == 'Italy':
        data[['new_cases', 'new_cases_per_million']] = data[['new_cases', 'new_cases_per_million']].shift(-1)
    data['NCI'] = data['new_cases_per_million'].rolling(DT_int).sum()/10
    data['PPT'] = (data['new_cases'].divide(data['new_tests'])*100).rolling(DT_int).mean()
    latest_date = get_latest_available_date(data)

    return data, latest_date

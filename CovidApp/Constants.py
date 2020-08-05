import pandas as pd
from datetime import timedelta
from datetime import datetime

cols = ['date', 'new_cases_per_million', 'new_cases', 'new_tests', 'population', 'continent', 'location']
bg='white'

NCI_max = 20
PPT_max = 5
DT_int = 14
today = pd.to_datetime('today').date()
yday = today - timedelta(days=1)
begin_day = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
dates = pd.date_range(begin_day, yday, freq='1D')
dates_dict = {i : fecha for i, fecha in enumerate(dates)}
DT = timedelta(days=DT_int)

Z = 12

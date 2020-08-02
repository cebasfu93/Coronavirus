import pandas as pd
from datetime import timedelta

bg='white'

NCI_max = 20
PPT_max = 5
DT_int = 14
today = pd.to_datetime('today').date()
yday = today - timedelta(days=1)
DT = timedelta(days=DT_int)

Z = 12

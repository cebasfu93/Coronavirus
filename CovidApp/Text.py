from Constants import *

info_txt1 = "The Norwegian state uses two metrics to determine\nwhether if quarantine is required upon entry from a specific country:\n\n\
The total number of new cases per 100,000 inhabitants in the last 14 days (NCI)\n \
The percentage of positive tests per week averaged for the last 2 weeks (PPT)\n\n \
In order for the Norwegian state to consider a country as\na high-incidence (i.e., high-risk) area, the country must have:\n"

info_txt2 = "NCI  > {:d}\n\
PPT >  {:d}\n\n".format(NCI_max, PPT_max)

info_txt3 = "-------------------------------------------------------------------------------------------------------------------\n"

question_txt = 'Which country would you like to assess?'

country_default = "Italy"

latest_date_txt = "\nLatest date available: {}"

metrics_txt = "NCI: {:.1f}\nPPT: {:.2f}\n"

date_min_txt = 'Minimum date to plot'
date_max_txt = 'Maximum date to plot'

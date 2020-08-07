from Constants import *

info_txt1 = "The Norwegian state uses two metrics to determine\nwhether if quarantine is required upon entry from a specific country:\n\n\
The total number of new cases per 100,000 inhabitants in the last 14 days (NCI)\n \
The percentage of positive tests per week averaged for the last 2 weeks (PPT)\n\n \
In order for the Norwegian state to consider a country as\na high-incidence (i.e., high-risk) area, the country must have:\n"

info_txt2 = "NCI  > {:d}\nPPT >  {:d}\n".format(NCI_max, PPT_max)

info_txt3 = " ------------------------------------------------------------------------------------------------------------------\n"

question_txt = 'Which country would you like to assess?'

country_default = "Select"

latest_data_txt = "\nLatest data available:"
latest_nci_txt = "NCI: {:.2f}   ({})"
latest_ppt_txt = "PPT: {:.2f}   ({})\n"

date_min_txt = 'Minimum date to plot'
date_max_txt = 'Maximum date to plot'

country_warn = "Please select a country"
popup_close = "Ok"

developer_txt = "Developed by Sebastian Franco Ulloa"
website_txt = "www.sebastianfu.com"

data_origin_txt = "Data from Our World in Data"
data_website_txt = "www.ourworldindata.org"

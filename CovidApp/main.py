from tkinter import *
from datetime import date
import pandas as pd
import os

def get_latest_available_date(country_df):
    mask_completeness = country_df.isna().sum(axis=1)==0
    latest_avail = country_df.loc[mask_completeness].iloc[-1].date
    return latest_avail

covid = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
covid = covid[covid.continent=='Europe']
countries = covid.location.unique()
today = date.today().strftime("%Y-%m-%d")
os.system('clear')

root = Tk()
root.title("Norwegian quarantine criteria")
root.geometry("600x600")
info_txt1 = "The Norwegian state uses two metrics to determine\nwhether if quarantine is required upon entry from a specific country:\n\n\
The number of new cases per 100,000 inhabitants (NCI)\n \
The percentage of positive tests (PPT)\n\n \
In order for the Norwegian state to consider a country as\na high-incidence (i.e., high-risk) area, the country must have:\n"
info_txt2 = "NCI > 20 for two weeks\n \
PPT > 5% for two weeks\n"
info_txt3 = "-------------------------------------------------------------------------------------------------------------------\n"
info_label1 = Label(root, text=info_txt1, font='Arial 12').grid(column=1, row=1)
info_label2 = Label(root, text=info_txt2, font='Arial 12 bold').grid(column=1, row=2)
info_label3 = Label(root, text=info_txt3, font='Arial 12').grid(column=1, row=3)

country_label = Label(root, text='Which country would you like to assess?', font='Arial 13 italic')
country_label.grid(column=1, row=4)

country_entry = StringVar()
country_entry.set("Italy")
country_drop = OptionMenu(root, country_entry, *countries)
country_drop.grid(column=1, row=5)

metric_txt, date_txt = StringVar(), StringVar()
metric_txt.set('')
date_txt.set('')
date_label = Label(root, textvariable=date_txt, font='Arial 12')
metric_label = Label(root, textvariable=metric_txt, font='Arial 12 bold')
date_label.grid(column=1, row=7)
metric_label.grid(column=1, row=8)

def assess_norwegian_entry():
    metric_txt.set('')
    date_txt.set('')
    root.update()
    country_df = covid[covid.location==country_entry.get()][['date', 'new_cases','new_tests','new_cases_per_million']]
    latest_date = get_latest_available_date(country_df)
    #country_df_today = country_df[country_df.date == today]
    country_df_latest = country_df[country_df.date == latest_date]
    NCI = float(country_df_latest['new_cases_per_million']/10)
    PPT = float(country_df_latest['new_cases']/country_df_latest['new_tests']*100)
    date_txt.set("\nLatest date available: {}".format(latest_date))
    metric_txt.set("\nNCI: {:.1f}".format(NCI)+"\n"+ "PPT: {:.2f}".format(PPT))
    return 0

go_button = Button(root, text='Go!', command=assess_norwegian_entry)
go_button.grid(column=1, row=6)

root.mainloop()

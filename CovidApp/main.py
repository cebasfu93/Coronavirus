from tkinter import *
from datetime import date
import pandas as pd
import os
from Text import *
from Constants import *
from Processing import import_covid, get_latest_available_date, assess_norwegian_metrics
from Plotting import from_rgb, plot_metrics


covid = import_covid()
countries = covid.location.unique()
today = date.today().strftime("%Y-%m-%d")
#os.system('clear')

root = Tk()
root.configure(bg='white')
root.title("Norwegian quarantine criteria")
root.geometry("1200x600")

info_label1 = Label(root, bg=bg, text=info_txt1, font='Arial 12').grid(column=1, row=1)
info_label2 = Label(root, bg=bg, text=info_txt2, font='Arial 12 bold').grid(column=1, row=2)
info_label3 = Label(root, bg=bg, text=info_txt3, font='Arial 12').grid(column=1, row=3)

country_label = Label(root, bg=bg, text=question_txt, font='Arial 13 italic')
country_label.grid(column=1, row=4)

country_entry = StringVar()
country_entry.set(country_default)
country_drop = OptionMenu(root, country_entry, *countries)
country_drop.config(bg=from_rgb((0.7,1,1)))
print(dict(country_drop['menu'].__dict__.items()))
country_drop.grid(column=1, row=5)

metric_txt, date_txt = StringVar(), StringVar()
metric_txt.set('')
date_txt.set('')
date_label = Label(root, bg=bg, textvariable=date_txt, font='Arial 12')
metric_label = Label(root, bg=bg, textvariable=metric_txt, font='Arial 12 bold')
date_label.grid(column=1, row=7)
metric_label.grid(column=1, row=8)

def show_metrics():
    metric_txt.set('')
    date_txt.set('')
    root.update()
    data, latest_date = assess_norwegian_metrics(covid, country_entry.get())
    date_txt.set(latest_date_txt.format(latest_date.strftime("%b %d, %Y")))
    nci, ppt = data.loc[latest_date, 'NCI'], data.loc[latest_date, 'PPT']
    metric_txt.set(metrics_txt.format(nci, ppt))

    plot_metrics(root, data)
    return 0

go_button = Button(root, bg=from_rgb((1,0.7,1)), text='Go!', command=show_metrics)
go_button.grid(column=1, row=6)

root.mainloop()

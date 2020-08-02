from tkinter import *
from datetime import date
from datetime import datetime
import pandas as pd
import os
from Text import *
from Constants import *
from Processing import import_covid, get_latest_available_date, assess_norwegian_metrics
from Plotting import from_rgb, plot_metrics

def show_metrics():
    metric_txt.set('')
    date_txt.set('')
    root.update()
    data, latest_date = assess_norwegian_metrics(covid, country_entry.get())
    date_txt.set(latest_date_txt.format(latest_date.strftime("%b %d, %Y")))
    nci, ppt = data.loc[latest_date, 'NCI'], data.loc[latest_date, 'PPT']
    metric_txt.set(metrics_txt.format(nci, ppt))

    plot_metrics(root, data)

    xmin_slider.grid(column=1, row=10)
    xmax_slider.grid(column=1, row=12)
    apply_button.grid(column=1, row=13)
    xmin_label.grid(column=1, row=9, sticky=W, padx=40)
    xmax_label.grid(column=1, row=11, sticky=W, padx=40)
    return 0

def update_slider_min(value):
    xmin = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmin_slider.config(label=xmin)

def update_slider_max(value):
    xmax = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmax_slider.config(label=xmax)

def update_plots():
    date_ini = dates_dict[xmin_slider.get()]
    date_fin = dates_dict[xmax_slider.get()]
    data, latest_date = assess_norwegian_metrics(covid, country_entry.get())
    plot_metrics(root, data, date_ini=date_ini, date_fin=date_fin)

covid = import_covid()
countries = covid.location.unique()
today = date.today().strftime("%Y-%m-%d")
#os.system('clear')

root = Tk()
root.iconbitmap('images/SFU.ico')
root.configure(bg='white')
root.title("Norwegian quarantine criteria")
#root.geometry("1200x800")

info_label1 = Label(root, bg=bg, text=info_txt1, font='Arial 12').grid(column=1, row=1)
info_label2 = Label(root, bg=bg, text=info_txt2, font='Arial 12 bold').grid(column=1, row=2)
info_label3 = Label(root, bg=bg, text=info_txt3, font='Arial 12').grid(column=1, row=3)

country_label = Label(root, bg=bg, text=question_txt, font='Arial 13 italic')
country_label.grid(column=1, row=4)

country_entry = StringVar()
country_entry.set(country_default)
country_drop = OptionMenu(root, country_entry, *countries)
country_drop.config(bg=from_rgb((0.7,1,1)), font='Arial 12', activebackground=from_rgb((0.5,0.8,0.9)), width=11, borderwidth=2)
country_drop.grid(column=1, row=5)

go_button = Button(root, bg=from_rgb((1,0.7,1)), text='Go!', command=show_metrics, font='Arial 12', activebackground=from_rgb((0.8,0.5,0.8)), width=15, relief='solid', borderwidth=1.5)
go_button.grid(column=1, row=6)

metric_txt, date_txt = StringVar(), StringVar()
metric_txt.set('')
date_txt.set('')
date_label = Label(root, bg=bg, textvariable=date_txt, font='Arial 12')
metric_label = Label(root, bg=bg, textvariable=metric_txt, font='Arial 12 bold')
date_label.grid(column=1, row=7)
metric_label.grid(column=1, row=8)

date_min = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
date_max = yday
dates = pd.date_range(date_min, date_max, freq='1D')
dates_dict = {i : fecha for i, fecha in enumerate(dates)}
xmin_label = Label(root, text=date_min_txt, bg=bg, font='Arial 12', justify=LEFT)
xmin_slider = Scale(root, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_min, length=500, label=datetime.strftime(date_min, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)))
xmin_slider.set(min(dates_dict))
xmax_label = Label(root, text=date_max_txt, bg=bg, font='Arial 12', justify=LEFT)
xmax_slider = Scale(root, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_max, length=500, label=datetime.strftime(date_max, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)))
xmax_slider.set(max(dates_dict))
apply_button = Button(root, bg=from_rgb((1,0.7,1)), text='Apply changes', command=update_plots, font='Arial 12', activebackground=from_rgb((0.8,0.5,0.8)), width=15, relief='solid', borderwidth=1.5)

root.mainloop()

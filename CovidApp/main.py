from tkinter import filedialog
from tkinter import *
from datetime import date
from datetime import datetime
import pandas as pd
import os
from Text import *
from Constants import *
from Processing import import_covid, get_latest_available_date, assess_norwegian_metrics
from Plotting import from_rgb, plot_metrics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_metrics():
    global date_min
    global date_max
    date_min = dates_dict[xmin_slider.get()]
    date_max = dates_dict[xmax_slider.get()]

    data, latest_date_nci, latest_date_ppt = assess_norwegian_metrics(covid, country_entry.get())
    data_label.grid_forget()
    nci_label.grid_forget()
    ppt_label.grid_forget()
    data_txt.set(latest_data_txt)
    if latest_date_nci != None:
        nci = data.loc[latest_date_nci, 'NCI']
        nci_txt.set(latest_nci_txt.format(nci, latest_date_nci.strftime("%b %d, %Y")))
    else:
        nci_txt.set("Not enough information available to calculate NCI in this country")
    if latest_date_ppt != None:
        ppt = data.loc[latest_date_ppt, 'PPT']
        ppt_txt.set(latest_ppt_txt.format(ppt, latest_date_ppt.strftime("%b %d, %Y")))
    else:
        ppt_txt.set("Not enough information available to calculate PPT in this country")
    data_label.grid(column=1, row=7)
    nci_label.grid(column=1, row=8)
    ppt_label.grid(column=1, row=9)

    global plots_tk
    plots_tk.get_tk_widget().grid_forget()
    plots_tk = plot_metrics(root, data, date_ini=date_min, date_fin=date_max)
    plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=15)

def update_slider_min(value):
    xmin = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmin_slider.config(label=xmin)

def update_slider_max(value):
    xmax = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmax_slider.config(label=xmax)

def save_data():
    data, latest_date_nci, latest_date_ppt = assess_norwegian_metrics(covid, country_entry.get())
    data = data.loc[:,['new_cases_per_million', 'new_tests', 'population', 'new_cases', 'NCI', 'PPT']]
    root.filename = filedialog.asksaveasfilename(initialdir="~", title="Save file as", filetypes=(("csv files","*.csv"),("all files","*.*")))
    data.to_csv(root.filename)

root = Tk()
root.iconbitmap('images/SFU.ico')
root.configure(bg='white')
root.title("Norwegian quarantine criteria")
#root.geometry("1200x800")

covid = import_covid()
countries = covid.location.sort_values().unique()
date_min = begin_day
date_max = yday

info_label1 = Label(root, bg=bg, text=info_txt1, font='Arial 12')
info_label2 = Label(root, bg=bg, text=info_txt2, font='Arial 12 bold')
info_label3 = Label(root, bg=bg, text=info_txt3, font='Arial 12')

country_label = Label(root, bg=bg, text=question_txt, font='Arial 13 italic')
country_entry = StringVar()
country_entry.set(country_default)
country_drop = OptionMenu(root, country_entry, *countries)
country_drop.config(bg=from_rgb((0.7,1,1)), font='Arial 12', activebackground=from_rgb((0.5,0.8,0.9)), width=11, borderwidth=2)

go_button = Button(root, bg=from_rgb((1,0.7,1)), text='Go!', command=show_metrics, font='Arial 12', activebackground=from_rgb((0.8,0.5,0.8)), width=15, relief='solid', borderwidth=1.5)

data_txt, nci_txt, ppt_txt = StringVar(), StringVar(), StringVar()
data_txt.set('\nSelect a contry to display information')
nci_txt.set('')
ppt_txt.set('\n')
data_label = Label(root, bg=bg, textvariable=data_txt, font='Arial 12')
nci_label = Label(root, bg=bg, textvariable=nci_txt, font='Arial 12 bold')
ppt_label = Label(root, bg=bg, textvariable=ppt_txt, font='Arial 12 bold')

xmin_label = Label(root, text=date_min_txt, bg=bg, font='Arial 12', justify=LEFT)
xmin_slider = Scale(root, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_min, length=500, label=datetime.strftime(date_min, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)))
xmin_slider.set(min(dates_dict))
xmax_label = Label(root, text=date_max_txt, bg=bg, font='Arial 12', justify=LEFT)
xmax_slider = Scale(root, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_max, length=500, label=datetime.strftime(date_max, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)))
xmax_slider.set(max(dates_dict))

apply_button = Button(root, bg=from_rgb((1,0.7,1)), text='Apply changes', command=show_metrics, font='Arial 12', activebackground=from_rgb((0.8,0.5,0.8)), width=15, relief='solid', borderwidth=1.5)
export_button = Button(root, bg=from_rgb((0.6,0.9,0.6)), text='Save data (.csv)', command=save_data, font='Arial 12', activebackground=from_rgb((0.3,0.6,0.3)), width=15, relief='solid', borderwidth=1.5)

info_label1.grid(column=1, row=1)
info_label2.grid(column=1, row=2)
info_label3.grid(column=1, row=3)
country_label.grid(column=1, row=4)
country_drop.grid(column=1, row=5)
go_button.grid(column=1, row=6)
data_label.grid(column=1, row=7)
nci_label.grid(column=1, row=8)
ppt_label.grid(column=1, row=9)
xmin_label.grid(column=1, row=10, sticky=W, padx=40)
xmin_slider.grid(column=1, row=11)
xmax_label.grid(column=1, row=12, sticky=W, padx=40)
xmax_slider.grid(column=1, row=13)
apply_button.grid(column=1, row=14, sticky=W, padx=40)
export_button.grid(column=1, row=14, sticky=E, padx=40)

bland_df = pd.DataFrame(0, columns=cols+['NCI','PPT'], dtype='int',index=[datetime.strptime('2020-01-01', '%Y-%m-%d')])
plots_tk = plot_metrics(root, bland_df)
plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=15)

root.mainloop()

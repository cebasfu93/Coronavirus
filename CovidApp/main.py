from tkinter import filedialog
from tkinter import *
from datetime import date
from datetime import datetime
import pandas as pd
import os
from Text import *
from Constants import *
from Processing import import_covid, get_latest_available_date, assess_norwegian_metrics
from Plotting import from_rgb, hex_to_rgb, plot_metrics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import webbrowser

def popup_country_select_warning():
    popup = Toplevel()
    popup.iconbitmap('images/SFU.ico')
    popup.configure(bg='white')
    popup.title('Invalid request')
    popup.geometry('400x300')
    frame = Frame(popup, bg=bg, relief='groove', padx=75, pady=75, borderwidth=2)
    popup_label = Label(frame, bg=bg, text=country_warn, font='Arial 16')
    popup_button = Button(frame, bg=from_rgb((0.8,0.8,0.8)), activebackground=from_rgb((0.5,0.5,0.5)), text=popup_close, command=popup.destroy, font='Arial 14', width=15, relief='solid', borderwidth=1.5)
    frame.pack(expand=True)
    popup_label.pack()
    popup_button.pack(pady=30)

def hover_in_color_change(event):
    rgb = hex_to_rgb(event.widget["bg"])
    rgb = (c/1.3 for c in rgb)
    event.widget["bg"] = from_rgb(rgb)

def hover_out_color_change(event):
    rgb = hex_to_rgb(event.widget["bg"])
    rgb = tuple(c*1.3/(255*255) for c in rgb)
    event.widget["bg"] = from_rgb(rgb)

def open_website(event):
    webbrowser.open_new(event.widget.cget("text"))

def show_metrics():
    if country_entry.get() != country_default:
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
        data_label.grid(column=1, row=4, pady=(0,5))
        nci_label.grid(column=1, row=5, pady=(0,2.5))
        ppt_label.grid(column=1, row=6, pady=(0,15))

        global plots_tk
        plots_tk.get_tk_widget().grid_forget()
        plots_tk = plot_metrics(root, data, date_ini=date_min, date_fin=date_max)
        plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=16, padx=(0,20), pady=10)

    else:
        popup_country_select_warning()

def update_slider_min(value):
    xmin = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmin_slider.config(label=xmin)

def update_slider_max(value):
    xmax = datetime.strftime(dates_dict[int(value)], "%b %d, %Y")
    xmax_slider.config(label=xmax)

def save_data():
    if country_entry.get() != country_default:
        data, latest_date_nci, latest_date_ppt = assess_norwegian_metrics(covid, country_entry.get())
        data = data.loc[:,['new_cases_per_million', 'new_tests', 'population', 'new_cases', 'NCI', 'PPT']]
        root.filename = filedialog.asksaveasfilename(initialdir="~", title="Save file as", filetypes=(("csv files","*.csv"),("all files","*.*")))
        data.to_csv(root.filename)
    else:
        popup_country_select_warning()

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

action_frame = Frame(root, bg=bg, bd=1, borderwidth=5, relief=RIDGE)
country_label = Label(action_frame, bg=bg, text=question_txt, font='Arial 13 italic')
country_entry = StringVar()
country_entry.set(country_default)
country_drop = OptionMenu(action_frame, country_entry, *countries)
country_drop.config(bg=from_rgb((0.7,1,1)), font='Arial 12', activebackground=from_rgb((0.5,0.8,0.9)), width=11, borderwidth=2)

go_button = Button(action_frame, bg=from_rgb((1,0.7,1)), text='Go!', command=show_metrics, font='Arial 12', activebackground=from_rgb((1,0.7,1)), width=15, relief='solid', borderwidth=1.5)
go_button.bind("<Enter>", hover_in_color_change)
go_button.bind("<Leave>", hover_out_color_change)

data_txt, nci_txt, ppt_txt = StringVar(), StringVar(), StringVar()
data_txt.set('Select a contry to display information')
nci_txt.set('')
ppt_txt.set('')
data_label = Label(action_frame, bg=bg, textvariable=data_txt, font='Arial 12')
nci_label = Label(action_frame, bg=bg, textvariable=nci_txt, font='Arial 12 bold')
ppt_label = Label(action_frame, bg=bg, textvariable=ppt_txt, font='Arial 12 bold')

xmin_label = Label(action_frame, text=date_min_txt, bg=bg, font='Arial 12', justify=LEFT)
xmin_slider = Scale(action_frame, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_min, length=500, label=datetime.strftime(date_min, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)), bd=1, borderwidth=2)
xmin_slider.set(min(dates_dict))
xmax_label = Label(action_frame, text=date_max_txt, bg=bg, font='Arial 12', justify=LEFT)
xmax_slider = Scale(action_frame, from_=min(dates_dict), to=max(dates_dict), resolution=1, orient=HORIZONTAL, showvalue=False, command=update_slider_max, length=500, label=datetime.strftime(date_max, "%b %d, %Y"), font='Arial 11', bg=bg, relief='groove', troughcolor=from_rgb((0.9,0.9,0.8)), bd=1, borderwidth=2)
xmax_slider.set(max(dates_dict))

apply_button = Button(action_frame, bg=from_rgb((1,0.7,1)), text='Apply changes', command=show_metrics, font='Arial 12', activebackground=from_rgb((1,0.7,1)), width=15, relief='solid', borderwidth=1.5)
apply_button.bind("<Enter>", hover_in_color_change)
apply_button.bind("<Leave>", hover_out_color_change)
export_button = Button(action_frame, bg=from_rgb((0.6,0.9,0.6)), text='Save data (.csv)', command=save_data, font='Arial 12', activebackground=from_rgb((0.6,0.9,0.6)), width=15, relief='solid', borderwidth=1.5)
export_button.bind("<Enter>", hover_in_color_change)
export_button.bind("<Leave>", hover_out_color_change)

wdt = 36
ref_frame = Frame(root, bg=bg)
dev_label = Label(ref_frame, text=developer_txt, width=wdt, height=1, bg=bg, font='Arial 10', anchor=W)
web_label = Label(ref_frame, text=website_txt, width=wdt, height=1,bg=bg, font='Arial 10 bold', anchor=W, fg=from_rgb((0.2,0.2,1.0)), cursor="hand2")
web_label.bind("<Button-1>", open_website)
data_origin_label = Label(ref_frame, text=data_origin_txt, width=wdt+1, height=1,bg=bg, font='Arial 10', anchor=E)
data_web_label = Label(ref_frame, text=data_website_txt, width=wdt+1, height=1,bg=bg, font='Arial 10 bold', anchor=E, fg=from_rgb((0.2,0.2,1.0)), cursor="hand2")
data_web_label.bind("<Button-1>", open_website)

info_label1.grid(column=1, row=1, pady=(20,0))
info_label2.grid(column=1, row=2)

action_frame.grid(column=1, row=3, rowspan=13, sticky="NESW", padx=20)
country_label.grid(column=1, row=1, ipady=10, pady=(10,0))
country_drop.grid(column=1, row=2, pady=(10,5))
go_button.grid(column=1, row=3, pady=(0,10))
data_label.grid(column=1, row=4, pady=(0,5))
nci_label.grid(column=1, row=5, pady=(0,2.5))
ppt_label.grid(column=1, row=6, pady=(0,15))
xmin_label.grid(column=1, row=7, sticky=W, padx=40)
xmin_slider.grid(column=1, row=8, pady=(0,5), padx=40)
xmax_label.grid(column=1, row=9, sticky=W, padx=40)
xmax_slider.grid(column=1, row=10, pady=(0,10), padx=40)
apply_button.grid(column=1, row=11, sticky=W, ipadx=20, padx=40, pady=(0,20))
export_button.grid(column=1, row=11, sticky=E, ipadx=20, padx=40, pady=(0,20))

ref_frame.grid(column=1, row=16, sticky="NESW", padx=20, pady=10, rowspan=2)
dev_label.grid(column=1, row=1, sticky=W, pady=0)
data_origin_label.grid(column=2, row=1, sticky=E, pady=0)
web_label.grid(column=1, row=2, sticky=W, pady=0)
data_web_label.grid(column=2, row=2, sticky=E, pady=0)

bland_df = pd.DataFrame(0, columns=cols+['NCI','PPT'], dtype='int',index=[datetime.strptime('2020-01-01', '%Y-%m-%d')])
plots_tk = plot_metrics(root, bland_df)
plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=16, padx=(0,20), pady=10)

root.mainloop()

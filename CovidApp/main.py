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
        data_label.grid(column=1, row=7)
        nci_label.grid(column=1, row=8)
        ppt_label.grid(column=1, row=9)

        global plots_tk
        plots_tk.get_tk_widget().grid_forget()
        plots_tk = plot_metrics(root, data, date_ini=date_min, date_fin=date_max)
        plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=16)

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
info_label3 = Label(root, bg=bg, text=info_txt3, font='Arial 12')

country_label = Label(root, bg=bg, text=question_txt, font='Arial 13 italic')
country_entry = StringVar()
country_entry.set(country_default)
country_drop = OptionMenu(root, country_entry, *countries)
country_drop.config(bg=from_rgb((0.7,1,1)), font='Arial 12', activebackground=from_rgb((0.5,0.8,0.9)), width=11, borderwidth=2)

go_button = Button(root, bg=from_rgb((1,0.7,1)), text='Go!', command=show_metrics, font='Arial 12', activebackground=from_rgb((1,0.7,1)), width=15, relief='solid', borderwidth=1.5)
go_button.bind("<Enter>", hover_in_color_change)
go_button.bind("<Leave>", hover_out_color_change)

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

dev_label = Label(root, text=developer_txt, bg=bg, font='Arial 10', justify=LEFT)
web_label = Label(root, text=website_txt, bg=bg, font='Arial 10 bold', justify=LEFT, fg=from_rgb((0.2,0.2,1.0)), cursor="hand2")
web_label.bind("<Button-1>", open_website)

data_origin_label = Label(root, text=data_origin_txt, bg=bg, font='Arial 10', justify=RIGHT)
data_web_label = Label(root, text=data_website_txt, bg=bg, font='Arial 10 bold', justify=RIGHT, fg=from_rgb((0.2,0.2,1.0)), cursor="hand2")
data_web_label.bind("<Button-1>", open_website)

apply_button = Button(root, bg=from_rgb((1,0.7,1)), text='Apply changes', command=show_metrics, font='Arial 12', activebackground=from_rgb((1,0.7,1)), width=15, relief='solid', borderwidth=1.5)
apply_button.bind("<Enter>", hover_in_color_change)
apply_button.bind("<Leave>", hover_out_color_change)
export_button = Button(root, bg=from_rgb((0.6,0.9,0.6)), text='Save data (.csv)', command=save_data, font='Arial 12', activebackground=from_rgb((0.6,0.9,0.6)), width=15, relief='solid', borderwidth=1.5)
export_button.bind("<Enter>", hover_in_color_change)
export_button.bind("<Leave>", hover_out_color_change)

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
dev_label.grid(column=1, row=15, sticky="WS", padx=40)
web_label.grid(column=1, row=16, sticky="WN", padx=40)
data_origin_label.grid(column=1, row=15, sticky="ES", padx=40)
data_web_label.grid(column=1, row=16, sticky="EN", padx=40)

bland_df = pd.DataFrame(0, columns=cols+['NCI','PPT'], dtype='int',index=[datetime.strptime('2020-01-01', '%Y-%m-%d')])
plots_tk = plot_metrics(root, bland_df)
plots_tk.get_tk_widget().grid(column=2, row=1, rowspan=16)

root.mainloop()

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from Constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def from_rgb(rgb):
    rgb = tuple(int(c*255) for c in rgb)
    return "#%02x%02x%02x" % rgb

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    lv = len(hex)
    return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def plot_metrics(gui, data, date_ini=begin_day, date_fin=yday):
    pop = data.loc[data.population.notna(),['population']].iloc[-1]
    dates = pd.date_range(date_ini, date_fin, periods=10)
    dates_mini = pd.date_range(date_ini, date_fin, periods=19)
    dateticks = [t.strftime('%b-%d') for t in dates]
    data_keep = data.loc[np.logical_and(data.index>=date_ini.strftime("%Y-%m-%d"), data.index<=date_fin.strftime("%Y-%m-%d"))]

    new_cases_warn = int(NCI_max*pop/(100000*DT_int))

    fig, axs = plt.subplots(figsize=(6,7.5), ncols=1, nrows=3, sharex=True)
    plots_tk = FigureCanvasTkAgg(fig, master=gui)

    for ax in axs:
        ax.tick_params('both', which='both', labelsize=Z, top=True, right=True, direction='in')
        ax.tick_params('both', which='major', length=9, width=1.3)
        ax.tick_params('both', which='minor', length=5, width=0.7)
        ax.set_xticks(dates)
        ax.set_xticks(dates_mini, minor=True)
        ax.set_xticklabels(dateticks, rotation=60)
        ax.set_xlim((dates[0], dates[-1]))

    #axs[0] -> New cases
    axs[0].set_ylabel('New cases', fontsize=Z)
    axs[0].set_ylim((0, max(new_cases_warn+100, data_keep.new_cases.max()+100)))
    axs[0].fill_between(data_keep.index, 0, data_keep.new_cases.rolling(DT_int, center=True).mean(), alpha=0.15, color=(0,0,0.7), zorder=1)
    axs[0].errorbar(data_keep.index, data_keep.new_cases.rolling(DT_int, center=True).mean(), lw=3.5, c=(0,0,0.7), label="2-week\nmoving average", zorder=2)
    axs[0].errorbar(data_keep.index, data_keep.new_cases, alpha=0.3, c=(0.1,0.1,0.9), fmt='o-', markevery=1, mec='k', mew=1.2, lw=1, label='Data records', zorder=3)
    l = axs[0].legend(fontsize=Z-2, shadow=True, fancybox=True, labelspacing=0.3, handlelength=1, handletextpad=0.6, borderpad=0.4)
    l.set_zorder(10)

    axs[0].grid()
    ax1 = axs[0].twinx()
    ax1.set_ylabel("Necessary daily cases\n-for two weeks-\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=40)
    ax1.axhline(new_cases_warn, lw=1.5, c=(0.2,0.2,0.2), ls='--', zorder=4)
    ax1.set_ylim((0, max(new_cases_warn+100, data_keep.new_cases.max()+100)))
    ax1.set_yticks([new_cases_warn])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))


    #axs[1] -> NCI
    axs[1].set_ylabel('NCI', fontsize=Z)
    axs[1].set_ylim((0, max(25, data_keep.NCI.max()+10)))
    axs[1].fill_between(data_keep.index, 0, data_keep.NCI, alpha=0.15, color=(1,0,0.7))
    axs[1].errorbar(data_keep.index, data_keep.NCI, lw=3.5, c=(0.7,0,0.4))
    axs[1].grid()
    ax1 = axs[1].twinx()
    ax1.axhline(20, lw=1.5, c=(0.2,0.2,0.2), ls='--')
    ax1.set_ylim((0, max(25, data_keep.NCI.max()+10)))
    ax1.set_yticks([20])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))
    ax1.set_ylabel("Necessary NCI\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=40)

    #axs[2] -> PPT
    axs[2].set_xlabel('Date', fontsize=Z)
    axs[2].set_ylabel('PPT (%)', fontsize=Z)
    axs[2].set_ylim((0, max(8, data_keep.PPT.max()+3)))
    axs[2].fill_between(data_keep.index, 0, data_keep.PPT, alpha=0.15, color=(0,0.9,0))
    axs[2].errorbar(data_keep.index, data_keep.PPT, lw=3.5, c=(0,0.7,0))#, label="2-week\nmoving average")
    axs[2].grid()

    ax1 = axs[2].twinx()
    ax1.axhline(5, lw=1.5, c=(0.2,0.2,0.2), ls='--')
    ax1.set_ylim((0, max(8, data_keep.PPT.max()+3)))
    ax1.set_yticks([5])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))
    ax1.set_ylabel("Necessary PPT\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=40)
    plt.tight_layout()

    return plots_tk

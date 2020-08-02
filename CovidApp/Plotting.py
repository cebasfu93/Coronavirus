import matplotlib.pyplot as plt
from Constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    rgb = tuple(int(c*255) for c in rgb)
    return "#%02x%02x%02x" % rgb

def plot_metrics(gui, data, date_ini='2020-01-01'):
    pop = data.loc[data.population.notna(),'population'].loc[yday]
    dates = pd.date_range(date_ini, yday, periods=10)
    dates_mini = pd.date_range(date_ini, yday, periods=19)
    dateticks = [t.strftime('%b-%d') for t in dates]
    data_keep = data.loc[data.index>date_ini]

    new_cases_warn = int(NCI_max*pop/(100000*DT_int))

    fig, axs = plt.subplots(figsize=(6,6), ncols=1, nrows=3, sharex=True)
    plots_tk = FigureCanvasTkAgg(fig, gui)
    plots_tk.get_tk_widget().grid(column=2, columnspan=5, row=1, rowspan=15)#, sticky="WENS")

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
    axs[0].set_ylim((0, data_keep.new_cases.max()+100))
    axs[0].fill_between(data_keep.index, 0, data_keep.new_cases.rolling(DT_int, center=True).mean(), alpha=0.15, color=(0,0,0.7))
    axs[0].errorbar(data_keep.index, data_keep.new_cases.rolling(DT_int, center=True).mean(), lw=3.5, c=(0,0,0.7), label="2-week\nmoving average")
    axs[0].errorbar(data_keep.index, data_keep.new_cases, alpha=0.3, c=(0.1,0.1,0.9), fmt='o-', markevery=1, mec='k', mew=1.2, lw=1, label='Data records')
    axs[0].legend(fontsize=Z-4, shadow=True, fancybox=True, labelspacing=0.3, handlelength=1, handletextpad=0.6, borderpad=0.4)
    axs[0].grid()
    ax1 = axs[0].twinx()
    ax1.set_ylabel("Necessary daily cases\n-for two weeks-\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=50)
    ax1.axhline(new_cases_warn, lw=1.5, c=(0.2,0.2,0.2), ls='--')
    ax1.set_ylim((0, data_keep.new_cases.max()+100))
    ax1.set_yticks([new_cases_warn])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))
    #plt.savefig("New_cases.png", format='png', dpi=300)
    #plt.show()

    #axs[1] -> NCI
    axs[1].set_ylabel('NCI', fontsize=Z)
    axs[1].set_ylim((0, max(25, data_keep.NCI.max()+10)))
    axs[1].fill_between(data_keep.index, 0, data_keep.NCI, alpha=0.15, color=(1,0,0.7))
    axs[1].errorbar(data_keep.index, data_keep.NCI, lw=3.5, c=(0.7,0,0.4))#, label="2-week\nmoving average")
    axs[1].grid()
    ax1 = axs[1].twinx()
    ax1.axhline(20, lw=1.5, c=(0.2,0.2,0.2), ls='--')
    ax1.set_ylim((0, max(25, data_keep.NCI.max()+10)))
    ax1.set_yticks([20])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))
    ax1.set_ylabel("Necessary NCI\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=50)
    #plt.savefig("NCI.png", format='png', dpi=300)
    #plt.show()

    #axs[2] -> PPT
    axs[2].set_xlabel('Date', fontsize=Z)
    axs[2].set_ylabel('PPT (%)', fontsize=Z)
    axs[2].set_ylim((0, max(8, data_keep.PPT.max()+3)))
    axs[2].fill_between(data_keep.index, 0, data_keep.PPT, alpha=0.15, color=(0,0.9,0))
    axs[2].errorbar(data_keep.index, data_keep.PPT, lw=3.5, c=(0,0.7,0))#, label="2-week\nmoving average")
    axs[2].grid()

    ax1 = axs[2].twinx()
    ax1.axhline(5, lw=1.5, c=(0.2,0.2,0.2), ls='--')
    ax1.set_ylim((0, max(5, data_keep.PPT.max()+3)))
    ax1.set_yticks([5])
    ax1.tick_params(labelsize=Z, labelcolor=(0.2,0.2,0.2))
    ax1.set_ylabel("Necessary PPT\nfor 'high incidence'", rotation=270, fontsize=Z-3, backgroundcolor=(0.9,0.9,0.9), labelpad=50)
    plt.tight_layout()
    #plt.savefig("PPT.png", format='png', dpi=300)
    #plt.show()
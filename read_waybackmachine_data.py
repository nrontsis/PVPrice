import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

# req = Request('https://www.energytrend.com/solar-price.html', headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()

def get_dataframe(list_of_frames):
    col_index = 0
    frame_index = 0
    while True:
        try:
            column = list_of_frames[frame_index][col_index]
            if column.str.contains("ThinFilm").any() and len(column) < 20:
                return list_of_frames[frame_index], True
            else:
                col_index += 1
        except AttributeError:
            col_index += 1
        except KeyError:
            col_index = 0
            frame_index += 1
        except IndexError:
            print("!!!!NO PRICES FOUND!!!!")
            return 0, False
        
def index_map(df, module_type):
    if module_type == "ThinFlim":
        index = np.where(df[0].str.contains("ThinFilm"))[0]
    elif module_type == "Mono PERC":
        index = np.where(df[0] == "Mono High Eff / PERC Module")[0]
    elif module_type == "Mono PERC (China)":
        index = np.where(df[0].str.find("Mono High Eff / PERC Module in China") == 0)[0]
    elif module_type == "Mono":
        index = np.where(df[0].str.contains("Mono Silicon Solar Module"))[0]
    elif module_type == "Poly High Efficiency":
        index = np.where(df[0].str.contains("Poly High Eff / PERC Module"))[0]
    elif module_type == "Poly (China)":
        index = np.where(df[0].str.contains("Poly Module in China"))[0]
    elif module_type == "Poly":
        index = np.where(
            np.logical_or(
                np.logical_or(
                    np.logical_or(df[0].str.contains("Poly Silicon Solar Module").values,
                    df[0].str.contains("Poly Solar Module").values),
                    np.logical_or(df[0].str.contains("Silicon Module Per Watt").values,
                    df[0].str.contains("Silicon Module Price Per Watt").values)
                ),
                np.logical_or(df[0].str.contains("Silicon PV Module Price Per Watt").values,
                df[0].str.contains("Silicon Solar Module").values)
            )
        )[0]
    else:
        index = -1
    
    try:
        index = index[0]
    except TypeError:
        pass
    except IndexError:
        pass

    return index

def save_unique_ids(dir):
    names = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                print("Processing: ", filepath)
                try:
                    frame, success = get_dataframe(pd.read_html(filepath))
                    names = list(set().union(frame[0].values, names))
                except ValueError:
                    print("!!!!NO TABLES FOUND!!!!")

    with open('unique_names.txt', 'w') as f:
        for name in names:
            f.write("%s\n" % name)


def extract_prices(df, index):
    try:
        high_price = float(df[1][index])
        low_price = float(df[2][index])
        mean_price = float(df[3][index])
    except ValueError:
        return np.NaN, np.NaN, np.NaN

    if not np.isnan(high_price):
        assert(high_price > low_price)
        assert(mean_price > low_price)
        assert(high_price > mean_price)

    return high_price, low_price, mean_price
'''
df = pd.DataFrame(columns=['timestamp',
    'ThinFlim_high', 'ThinFlim_low', 'ThinFlim_mean',
    'Mono PERC_high', 'Mono PERC_low', 'Mono PERC_mean',
    'Mono PERC (China)_high', 'Mono PERC (China)_low', 'Mono PERC (China)_mean',
    'Mono_high', 'Mono_low', 'Mono_mean',
    'Poly High Efficiency_high', 'Poly High Efficiency_low', 'Poly High Efficiency_mean',
    'Poly (China)_high', 'Poly (China)_low', 'Poly (China)_mean',
    'Poly_high', 'Poly_low', 'Poly_mean',
    ]
)
i = 0
for root, dirs, files in os.walk("websites/"):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            print("Processing: ", filepath)
            try:
                frame, success = get_dataframe(pd.read_html(filepath))
                if success:
                    datetime = pd.to_datetime(root.split('/')[2])
                    data = [datetime]
                    for module_type in ["ThinFlim", "Mono PERC", "Mono PERC (China)", "Mono", "Poly High Efficiency", "Poly (China)", "Poly"]:
                        index = index_map(frame, module_type)
                        if index >= 0:
                            h, l, m = extract_prices(frame, index)
                        else:
                            h, l, m = np.NaN, np.NaN, np.NaN
                        data.append(h); data.append(l); data.append(m)
                    df.loc[i] = data
                    i += 1
                df.to_csv('data.csv')
            except ValueError:
                print("!!!!NO TABLES FOUND!!!!")
df = df.sort_values('timestamp')
df = df.set_index('timestamp')
df.to_csv('data.csv')
df.to_pickle('data.pkl')
'''
df = pd.read_pickle('data.pkl')

def plot_prices(df, module_type):
    m = df[module_type + '_mean']
    h = df[module_type + '_high']
    l = df[module_type + '_low']
    fig = plt.figure(figsize=(6, 3.5))
    ax = fig.add_subplot(111)
    ax.semilogy(df.index, m, 'b', lw=2)
    ax.fill_between(df.index, l, h, color='blue', alpha=0.2)
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10, subs=np.arange(2, 10, step=1.0)))
    # ax.yaxis.set_major_locator(ticker.LogLocator(base=10, subs='all'))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))
    plt.ylim((0.2, 2.25))
    # ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.LogFormatter(labelOnlyBase=False, minor_thresholds=(100, 0.01)))
    ax.tick_params(axis='both', which='both')
    years = mdates.YearLocator()   # every year
    yearsFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    # months = mdates.MonthLocator()  # every month
    # ax.xaxis.set_minor_locator(months)
    plt.grid(True, 'both')
    plt.xlabel('Time')
    plt.ylabel('Price ($/Watt)')
    plt.title('Historical Prices of ' + module_type + ' Modules')
    fig.savefig(module_type + ".pdf", bbox_inches='tight')
    
    return fig

for module_type in ["ThinFlim", "Mono PERC", "Mono PERC (China)", "Mono", "Poly High Efficiency", "Poly (China)", "Poly"]:
    fig = plot_prices(df, module_type)

plt.show()
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
        

def extract_prices(df):
    index = np.where(df[0].str.contains("ThinFilm"))[:][0]
    high_price = float(df[1][index])
    low_price = float(df[2][index])
    mean_price = float(df[3][index])
    assert(high_price > low_price)
    assert(mean_price > low_price)
    assert(high_price > mean_price)
    return high_price, low_price, mean_price

df = pd.DataFrame(columns=['timestamp', 'thinfilm_high', 'thinfilm_low', 'thinfilm_mean'])
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
                    h, l, m = extract_prices(frame)
                    df.loc[i] = (datetime, h, l, m)
                    i += 1
            except ValueError:
                print("!!!!NO TABLES FOUND!!!!")
df = df.sort_values('timestamp')
df = df.set_index('timestamp')
df.to_pickle('data.pkl')


df = pd.read_pickle('data.pkl')

def plot_prices(time, mean, high, low):
    fig = plt.figure(figsize=(6, 3.5))
    ax = fig.add_subplot(111)
    ax.semilogy(df.index, df['thinfilm_mean'], 'b', lw=2)
    ax.fill_between(df.index, df['thinfilm_low'], df['thinfilm_high'], color='blue', alpha=0.2)
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10, subs=np.arange(1, 10)+0.5))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    years = mdates.YearLocator()   # every year
    yearsFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    # months = mdates.MonthLocator()  # every month
    # ax.xaxis.set_minor_locator(months)
    plt.grid(True, 'both')
    plt.xlabel('Time')
    plt.ylabel('Price ($/Watt)')
    plt.title('Historical Prices of Thin Film Module Prices (PVInsights.com)')
    return fig

fig = plot_prices(df.index, df['thinfilm_mean'], df['thinfilm_high'], df['thinfilm_low'])
fig.savefig("thin_film.pdf", bbox_inches='tight')
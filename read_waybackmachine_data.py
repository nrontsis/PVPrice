import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
import os
import matplotlib.pyplot as plt

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
plt.semilogy(df['timestamp'], df['thinfilm_mean'])
# plt.semilogy(df['timestamp'], df['thinfilm_low'])
plt.show()
import pdb; pdb.set_trace()
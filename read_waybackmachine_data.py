import pandas as pd
from urllib.request import Request, urlopen

# req = Request('https://www.energytrend.com/solar-price.html', headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()

def get_dataframe(list_of_frames):
    col_index = 0
    frame_index = 0
    while True:
        try:
            column = list_of_frames[frame_index][col_index]
            if column.str.contains("ThinFilm").any() and len(column) < 10:
                print(index)
                return list_of_frames[frame_index]
            else:
                col_index += 1
        except AttributeError:
            col_index += 1
        except KeyError:
            col_index = 0
            frame_index += 1
        # except IndexError:
            # Not Found any frame with ThinFilm Module Prices

    

import os
for root, dirs, files in os.walk("websites/"):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            print("Processing: ", filepath)
            frame = get_dataframe(pd.read_html(filepath))
            print(frame)
            import pdb; pdb.set_trace()p

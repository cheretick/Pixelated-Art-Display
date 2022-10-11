from numpy import append
import pandas as pd
import pickle

# grabs commons resolutions and saves them in resolutions list
url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
table = pd.read_html(url)[0]
table.columns = table.columns.droplevel()

# saves resolutions up to 1080p in resolutions.data
res = []
for index, row in table[["W", "H"]].iterrows():
    res.append([row["W"], row["H"]])

newRes = []

for resolution in res:
    newRes.append(resolution)
    if resolution == [1920, 1080]:
        break

with open('./resolutions.data', 'wb') as fileHandle:
    pickle.dump(newRes, fileHandle)
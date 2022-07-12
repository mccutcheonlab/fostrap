# %%
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

import trompy as tp

folder = "../"
# %%
with open(folder + "fostrap_metafile.csv", "r") as f:
    r = csv.writer(f)
    header = f.readlines()[0]
    f.seek(0)
    metafilerows = f.readlines()[1:]

mouserows = []
for i in metafilerows:
    mouserows.append(i.split(','))

def get_cell_data(mouse, cells, normalize_to_area=False):

    # Use these when selecting data from source folders, not repository
    # subfolder = "\\nutil_{}\\Reports\\{}_{}_RefAtlasRegions\\{}_{}_RefAtlasRegions.csv".format(cells, mouse, cells, mouse, cells)
    # folder="D:\\Test Data\\fostrap\\"

    folder = "../data/"
    subfolder = "_{}_RefAtlasRegions.csv".format(cells)

    with open(folder+mouse+subfolder, "r") as f:
        r = csv.writer(f)
        header = f.readlines()[0]
        f.seek(0)
        filerows = f.readlines()[1:]

    tablerows = []
    for i in filerows:
        tablerows.append(i.split(';'))

    nutil_data = {}
    for row in tablerows:
        key=row[1]
        object_count=row[5]
        area=row[2]

        if normalize_to_area:
            try:
                nutil_data[key]=[int(object_count) / int(area)]
            except ZeroDivisionError:
                nutil_data[key]=0
        else:
            nutil_data[key]=[int(object_count)]
    
    df = pd.DataFrame.from_dict(nutil_data)

    return df

def read_in_data(cells, normalize_to_area):

    cols = ["mouse", "diet", "sex", "solution1", "solution2", "celltype"]
    df = pd.DataFrame()

    for row in mouserows:
        df_id = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], cells]], columns=cols)
        try:
            df_cells = get_cell_data(row[0], cells, normalize_to_area=False)
            print("Yay for {}".format(row[0]))
        except FileNotFoundError:
            print("Data for {} do not seem to be available yet.".format(row[0]))
            continue
        
        df_mouse = pd.concat([df_id, df_cells], axis=1)
        df_mouse.set_index("mouse", drop=True, inplace=True)
        
        if not df.empty:
            df = pd.concat([df, df_mouse], axis=0)
        else:
            df  = df_mouse
    
    return df
# %%
df_trap = read_in_data("trap", False)
df_fos = read_in_data("fos", False)

df_area_trap = read_in_data("trap", True)
df_area_fos = read_in_data("fos", True)

# %%
df_cells = pd.concat([df_trap, df_fos])
df_area = pd.concat([df_area_trap, df_area_fos])


# %%

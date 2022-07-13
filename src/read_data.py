# %%
import csv
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

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
            scale_factor = (2.6**2)*1e6 # pixels per mm
            try:
                nutil_data[key]=[int(object_count) / (int(area)/scale_factor)]
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
            df_cells = get_cell_data(row[0], cells, normalize_to_area=normalize_to_area)
            print("Yay for {}".format(row[0]))
        except FileNotFoundError:
            print("Data for {} do not seem to be available yet.".format(row[0]))
            continue
        
        df_mouse = pd.concat([df_id, df_cells], axis=1)
        # df_mouse.set_index("mouse", drop=True, inplace=True)
        
        if not df.empty:
            df = pd.concat([df, df_mouse], axis=0)
        else:
            df  = df_mouse
    
    # df = df.reset_index()
    # idx_cols = df_new.columns[:6].to_list()
    df.set_index(cols, inplace=True)
    
    return df
# %%
df_trap = read_in_data("trap", False)
df_fos = read_in_data("fos", False)
df_coloc = read_in_data("coloc", False)

df_area_trap = read_in_data("trap", True)
df_area_fos = read_in_data("fos", True)
df_area_coloc = read_in_data("coloc", True)

# %%
df_cells = pd.concat([df_trap, df_fos, df_coloc])
df_area = pd.concat([df_area_trap, df_area_fos, df_coloc])

def normalize_df(df):

    normalized_df = df.copy()
    for column in df.columns:
        if is_numeric_dtype(df[column]):
            if np.sum(df[column]) == 0:
                normalized_df.drop([column], axis=1, inplace=True)
                continue
            normalized_df[column] = (df[column] - df[column].mean()) /df[column].std()
            
    return normalized_df

df_cells_norm = normalize_df(df_cells)
df_area_norm = normalize_df(df_area)

# %%

df_new.xs(("nr", "casein"), level=("diet", "solution2"), axis=0, drop_level=False)
# %%

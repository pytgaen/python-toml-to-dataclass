import pandas as pd

data = [[1, 2, 3], [4, 5, 6]]
df_ref = pd.DataFrame(data, columns=["a", "b", "c"])
df_ref["origin_ref"] = "ref"

data = [[1, 2, 3], [44, 5, 6]]
df_1 = pd.DataFrame(data, columns=["a", "b", "c"])
df_1["origin_work"] = "work"

cols = df_ref.columns.tolist()
cols.remove("origin_ref")
dj = df_ref.merge(df_1, on=cols, how="outer")
print(dj)
print("")
dj = dj[dj["origin_ref"].isnull() | dj["origin_work"].isnull()]
dj["origin"] = dj['origin_ref'].combine_first(dj['origin_work'])
dj = dj.drop(columns=['origin_ref', 'origin_work'])
print(dj)

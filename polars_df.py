import polars as pl

data = [[1, 2, 3], [4, 5, 6]]
df_ref = pl.DataFrame(data, columns=["a", "b", "c"])
x = pl.Series("origin_ref", ["ref"] * df_ref.shape[0])
df_ref = df_ref.hstack([x])

data = [[1, 2, 3], [44, 5, 6]]
df_1 = pl.DataFrame(data, columns=["a", "b", "c"])
x = pl.Series("origin_work", ["work"] * df_ref.shape[0])
df_1 = df_1.hstack([x])

cols = df_ref.columns
cols.remove("origin_ref")
dj = df_ref.join(df_1, on=cols, how="outer")
print(dj)
print(dj.filter(pl.col("origin_ref").is_null() | pl.col("origin_work").is_null()))

# --8<-- [start:pokemon]
import polars as pl

# then let's load some csv data with information about pokemon
df = pl.read_csv(
    "https://gist.githubusercontent.com/ritchie46/cac6b337ea52281aa23c049250a4ff03/raw/89a957ff3919d90e6ef2d34235e6bf22304f3366/pokemon.csv"
)
print(df.head())
# --8<-- [end:pokemon]


# --8<-- [start:groupby]
out = df.select(
    [
        "Type 1",
        "Type 2",
        pl.col("Attack").mean().over("Type 1").alias("avg_attack_by_type"),
        pl.col("Defense")
        .mean()
        .over(["Type 1", "Type 2"])
        .alias("avg_defense_by_type_combination"),
        pl.col("Attack").mean().alias("avg_attack"),
    ]
)
print(out)
# --8<-- [end:groupby]

# --8<-- [start:operations]
filtered = df.filter(pl.col("Type 2") == "Psychic").select(
    [
        "Name",
        "Type 1",
        "Speed",
    ]
)
print(filtered)
# --8<-- [end:operations]

# --8<-- [start:sort]
out = filtered.with_columns(
    [
        pl.col(["Name", "Speed"]).sort_by("Speed", descending=True).over("Type 1"),
    ]
)
print(out)
# --8<-- [end:sort]

# --8<-- [start:rules]
# aggregate and broadcast within a group
# output type: -> Int32
pl.sum("foo").over("groups")

# sum within a group and multiply with group elements
# output type: -> Int32
(pl.col("x").sum() * pl.col("y")).over("groups")

# sum within a group and multiply with group elements
# and aggregate the group to a implode
# output type: -> List(Int32)
(pl.col("x").sum() * pl.col("y")).implode().over("groups")

# note that it will require an explicit `implode()` call
# sum within a group and multiply with group elements
# and aggregate the group to a list
# the flatten call explodes that list

# This is the fastest method to do things over groups when the groups are sorted
(pl.col("x").sum() * pl.col("y")).implode().over("groups").flatten()
# --8<-- [end:rules]

# --8<-- [start:examples]
out = df.sort("Type 1").select(
    [
        pl.col("Type 1").head(3).implode().over("Type 1").flatten(),
        pl.col("Name")
        .sort_by(pl.col("Speed"))
        .head(3)
        .implode()
        .over("Type 1")
        .flatten()
        .alias("fastest/group"),
        pl.col("Name")
        .sort_by(pl.col("Attack"))
        .head(3)
        .implode()
        .over("Type 1")
        .flatten()
        .alias("strongest/group"),
        pl.col("Name")
        .sort()
        .head(3)
        .implode()
        .over("Type 1")
        .flatten()
        .alias("sorted_by_alphabet"),
    ]
)
print(out)
# --8<-- [end:examples]

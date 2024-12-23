import pandas as pd

df = DataFrame()

# 基礎
# とりあえず脳死でまずはこれ
df.info() # dfのレコード数(行数)、各列のデータ型、欠損値の有無を確認
df.columns.tolist() # seriesのリスト変換
df.columns.value # seriesのnumpy変換

# 抽出
df.loc[:10, "fare"] # indexが数字ならlocでも数字指定可能。
df.iloc[:5, df.columns.get_loc("age")] # 列名、数字変換はcolumns.get_locを使用
df.query("sex=='female' & age >= 40") # queryを使えば列名だけに触れれば抽出可能
df.query("name.str.contains('Mrs')", engine='python') # 文字列含有データの抽出
df.select_dtypes(include='object') # 特定データ型（文字列）の列を抽出
df.select_dtypes(exclude="object") # object型以外の列を抽出
df.nunique() # 各列の要素数
df["embarked"].value_counts() # ユニーク要素とその出現回数、unique()は使う必要ないかも。。。

# 加工
df["sex"] = df["sex"].map({"male": 0, "female": 1})# mapは辞書がシリーズの要素を網羅できていないとnoneになる。
df["sex"] = df["sex"].replace({"male": 0, "female": 1}) # replaceは辞書がシリーズの要素を網羅できていないとそのままになる。
df["fare"] = df["fare"].round() # 小数点以下の四捨五入
df = df.drop("body", axis=1) # 列の削除
df.columns = ["name", "class", 'Biology', "Physics", "Chemistry"] # 列名をまとめて変更, renameで一部変更
df.dropna() # 欠損値を含む行の削除f
df.sample(frac=1) # 行のシャッフル表示。fracは抽出割合、nで個数で抽出指定可能.
df.sample(frac=1).reset_index() # indexの振り直し
df.duplicated().value_counts() # 重複行の確認。true, falseでまとめられる
df.name.str.upper() # seriesにstrをつけると文字列処理の関数群が使える
df.name = df.name.str.replace("Elisabeth", "") # 部分一致でおｋ, re使うやり方もあり
df.name = df.name.replace("Elisabeth", "") # 完全一致でないとだめ
df.name = df.name.str.rstrip() # 右側の空白削除、strip(両端), lstrip()もあり
df2 = df2.transpose() # 転置(df2 = df2.Tでもおｋ)
df["fare"].idxmax() # 最大値のインデックス
df["fare"].idxmin()
df["fare"].quantile([0, 0.25, 0.5, 0.75, 1.0]) # パーセンタイルの獲得
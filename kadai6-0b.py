import requests
import pandas as pd

APP_ID = "c91ed42dd1165c8fa5119240759e04233f9da99e"
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,                    # アプリケーションID
    "lang": "J",                        # 日本語
    "statsDataId": "0003410368",       # 観光統計調査（訪日外国人旅行者数）
    "metaGetFlg": "Y",                 # メタ情報を取得
    "explanationGetFlg": "Y",          # 統計表の概要説明を取得
    "annotationGetFlg": "Y",           # 注釈を取得
    "replaceSpChars": 0,               # 特殊文字の置換なし
    "cntGetFlg": "N",                  # 件数だけでなく実データを取得
    "sectionHeaderFlg": 1              # セクションヘッダ情報を取得
}

# APIからデータ取得
response = requests.get(API_URL, params=params)
data = response.json()

# データ部の取り出し
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

# メタ情報取得
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 各カテゴリIDを意味のある名称に置換
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名変換のディクショナリ
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    col_replace_dict['@' + class_obj['@id']] = class_obj['@name']

# 列名置換の実行
df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 表示
print(df)

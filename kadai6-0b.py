import requests
import pandas as pd

#石油製品需給動態統計調査 / 石油統計 年報

#石油は、日本の一次エネルギー供給の約４割を占めており、国民生活及び経済活動を支える社会基盤の構築のために不可欠となっています。また、日本では石油のほとんどが蒸留・精製によりガソリン等の石油製品に転換されて販売されています。
#本調査では、そんな石油製品について日本国内の需給の実態を明らかにするため、石油製品の製造業者、輸入業者等に対して毎月実施しており、石油製品別の月間受入量・払出量、国別の輸出入量、月末在庫量等を提供しています。
#本調査の結果は、行政はもとより民間企業でも広く活用されています。


APP_ID = "c91ed42dd1165c8fa5119240759e04233f9da99e"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID, # アプリケーションID
    "lang": "J",     # 言語：日本語
    "statsDataId": "0003171993",  # 統計表ID
    "metaGetFlg": "Y",            # メタ情報
    "explanationGetFlg": "Y",     # 統計表の概要説明を取得
    "annotationGetFlg": "Y",     # 注釈を取得
    "replaceSpChars": 0,         # 特殊文字を置換しない
    "cntGetFlg": "N",            # 件数のみの取得をしない
    "sectionHeaderFlg": 1        # セクションヘッダ情報を取得
}

response = requests.get(API_URL, params=params)
# Process the response
data = response.json()

# 統計データからデータ部取得
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# JSONからDataFrameを作成
df = pd.DataFrame(values)

# メタ情報取得
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 統計データのカテゴリ要素をID(数字の羅列)から、意味のある名称に変更する
for class_obj in meta_info:

    # メタ情報の「@id」の先頭に'@'を付与した文字列が、統計データの列名と対応している
    column_name = '@' + class_obj['@id']

    # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']

    # ディクショナリを用いて、指定した列の要素を置換
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 統計データの列名を変換するためのディクショナリを作成
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# ディクショナリに従って、列名を置換する
new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)

df.columns = new_columns
print(df)
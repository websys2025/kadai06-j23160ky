import requests

# アプリケーションID
APP_ID = "c91ed42dd1165c8fa5119240759e04233f9da99e"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID, # アプリケーションID（必須）
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
data = response.json()
print(data)
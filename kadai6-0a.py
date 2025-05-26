import requests

APP_ID = "c91ed42dd1165c8fa5119240759e04233f9da99e"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "lang": "J",
    "statsDataId": "0003171993",  # ← 小文字に修正！
    "metaGetFlg": "Y",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "replaceSpChars": 0,
    "cntGetFlg": "N",
    "sectionHeaderFlg": 1
}



#response = requests.get(API_URL, params=params)
response = requests.get(API_URL, params=params)
# Process the response
data = response.json()
print(data)
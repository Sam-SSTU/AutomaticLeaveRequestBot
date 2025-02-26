import requests
import json

# API 端点
url = "http://fk.ghcollege.cn/visitor/api/iep/weixin/api/ams/wx0b5c194a8eb873fc/book"

# 公共请求头
headers = {
    "Host": "fk.ghcollege.cn",
    "Accept": "application/json",
    "third-session": "efe1e329-1292-4006-ba43-ed6866fcfa7c",
    "WOKU-TOKEN": "Basic YXBwOmFwcA==",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Origin": "http://fk.ghcollege.cn",
    "Referer": "http://fk.ghcollege.cn/visitor/pages/ask/ask",
    "Connection": "keep-alive"
}

# 公共请求体（不带验证码）
data_no_verify = {
    "userCode": "24028307",
    "userName": "杨瀚琪",
    "phone": "15502165921",
    "subType": "1",
    "subTypeName": "事假",
    "startTime": 1741072824000,
    "endTime": 1741079086000,
    "adjustDes": "空课"
}

def send_request(data, test_case):
    response = requests.post(url, headers=headers, json=data)
    print(f"Test Case: {test_case}\nStatus Code: {response.status_code}\nResponse: {response.text}\n")



# 2. 发送 verifyCode=187709
data_2 = data_no_verify.copy()
data_2["verifyCode"] = "-0"
send_request(data_2, "verifyCode 187709")



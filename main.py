import requests
header_data={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
response=requests.get("https://tw.yahoo.com",headers=header_data)
print(response.text)

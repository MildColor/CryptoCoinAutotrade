# REST API
import requests

url = "https://api.upbit.com/v1/market/all"
resp = requests.get(url)
data = resp.json() #JSON 자바스크립트 로테이션이라는 타입을 파이썬에 딕셔너리나 기본데이터 타입으로 변환
print(len(data))
print(data)


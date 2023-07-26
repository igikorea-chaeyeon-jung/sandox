# 기상청 API 연동
import requests
import datetime
import json

vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

service_key = "TkQq1%2FuKX4F6381WyCXnCQ4AA8Del8lOsfF8MrZloNIVLVexGgrONTI7qO0MlDSHTBBeTfBtJjCaZHCWSofShw%3D%3D"

today = datetime.datetime.today()
base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜
base_time = "0800" # 날씨 값

nx = "60"
ny = "128"

payload = "serviceKey=" + service_key + "&" +\
    "dataType=json" + "&" +\
    "base_date=" + base_date + "&" +\
    "base_time=" + base_time + "&" +\
    "nx=" + nx + "&" +\
    "ny=" + ny

# 값 요청
res = requests.get(vilage_weather_url + payload)

items = res.json().get('response').get('body').get('items')
print(items)

#-----------------------------------------------------------------------
# json파일 hdfs에 저장
from hdfs import InsecureClient

def write_json_to_hdfs(json_data, hdfs_path):
    
    # HDFS 클라이언트 생성
    client = InsecureClient('http://54.180.83.185:50070', user='centos')

    # JSON 데이터를 HDFS에 쓰기
    with client.write(hdfs_path, overwrite=True, encoding='utf-8') as writer:
        writer.write(json.dumps(json_data))

if __name__ == "__main__":
    # 쓰고자 하는 JSON 데이터

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    # 쓰고자 하는 HDFS 경로
    hdfs_path = '/data/weather/data_weather_{now}.json'
    
    try:
        # JSON 데이터를 HDFS에 쓰기
        write_json_to_hdfs(items, hdfs_path)
        print("JSON 파일을 HDFS에 성공적으로 썼습니다.")
    except Exception as e:
        print("에러가 발생했습니다:", e)

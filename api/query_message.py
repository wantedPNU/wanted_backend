import aiohttp
import asyncio
import re
import urllib3
import sys
import os

# 현재 작업 디렉토리를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from keys import api_key

# InsecureRequestWarning 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 기본 URL 및 데이터 경로
url = "https://www.safetydata.go.kr"
dataName = "/V2/api/DSSP-IF-00247"

# 서비스 키
serviceKey = api_key.serviceKey

page_no = "548"

# 요청에 사용할 파라미터들
payloads = {
    "serviceKey": serviceKey,
    "returnType": "json",  # 데이터를 JSON 형식으로 반환
    "pageNo": page_no,       # 페이지 번호
    "numOfRows": "30",     # 한 페이지에 표시할 데이터 개수
}

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url + dataName, params=payloads) as response:
                data = await response.json()

                # 인상착의 리스트를 저장할 변수
                descriptions_list = []

                # 경찰청 지역정보를 추출하기 위한 정규 표현식
                police_station_pattern = re.compile(r'(\w+)경찰청')

                # '찾습니다'가 포함된 메시지 필터링 및 인상착의 추출
                for item in data['body']:
                    message = item['MSG_CN']
                    
                    # 경찰청 지역정보 추출
                    police_station_match = police_station_pattern.search(message)
                    police_station = police_station_match.group(1) if police_station_match else '지역정보 없음'
                    
                    if '찾습니다' in message:
                        description_start = message.find('-') + 1
                        description_end = message.find('\r\n')
                        if description_end == -1:  # \r\n이 없을 경우 문자열 끝까지 추출
                            description_end = len(message)
                        description = message[description_start:description_end].strip()

                        # 인상착의를 공백으로 분할하여 리스트로 변환
                        description_words = description.split(',')

                        # 숫자가 포함된 단어들을 걸러내고, 문자열로만 이루어진 단어들만 리스트에 포함
                        filtered_words = [word for word in description_words if not any(char.isdigit() for char in word)]

                        # 지역정보와 인상착의 리스트 추가
                        descriptions_list.append({
                            'region': police_station,
                            'description': filtered_words
                        })

                # 인상착의 리스트 출력
                print(descriptions_list)

            # 2분(120초) 대기
            await asyncio.sleep(120)

# 데이터 주기적 수집 시작
asyncio.run(fetch_data())

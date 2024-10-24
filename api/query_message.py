from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import aiohttp
import re
import urllib3
import datetime
from typing import List, Dict, Any
from keys import api_key

# InsecureRequestWarning 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 기본 URL 및 데이터 경로
url = "https://www.safetydata.go.kr"
dataName = "/V2/api/DSSP-IF-00247"

# 서비스 키
#serviceKey = api_key.serviceKey2
serviceKey = api_key.serviceKey2

# 요청에 사용할 파라미터들
payloads = {
    "serviceKey": serviceKey,
    "returnType": "json",  # 데이터를 JSON 형식으로 반환
    "numOfRows": "30",      # 한 페이지에 표시할 데이터 개수
}

router = APIRouter()

class Description(BaseModel):
    region: str
    description: List[str]
    creation_date: str

@router.get("/fetch-data", response_model=List[Description], tags=["Data Fetch"])
async def fetch_data():
    page_no = 670  # 페이지 번호를 함수 내부에 정의
    descriptions_list: List[Description] = []

    async with aiohttp.ClientSession() as session:
        while len(descriptions_list) < 5 and page_no > 0:
            payloads['pageNo'] = str(page_no)
            try:
                async with session.get(url + dataName, params=payloads) as response:
                    data = await response.json()

                    # 만약 data['body']가 None이거나 데이터가 없으면 페이지 번호를 줄이고 계속
                    if not data or 'body' not in data or data['body'] is None:
                        raise ValueError("Empty or invalid data")

                    # 경찰청 지역정보를 추출하기 위한 정규 표현식
                    police_station_pattern = re.compile(r'(\w+)경찰청')

                    # '찾습니다'가 포함된 메시지 필터링 및 인상착의 추출
                    for item in data['body']:
                        message = item.get('MSG_CN', '')
                        creation_date = item.get('CRT_DT', '날짜 없음')  # 생성일시(CRT_DT) 가져오기

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

                            # 지역정보와 인상착의 리스트 및 생성일시 추가
                            descriptions_list.append(Description(
                                region=police_station,
                                description=filtered_words,
                                creation_date=creation_date
                            ))

                            # 결과가 5개가 되면 종료
                            if len(descriptions_list) >= 5:
                                break

            except (ValueError, TypeError):
                # 예외 발생 시 페이지 번호를 줄이고 다시 시도
                page_no -= 1
                continue

            # 페이지 번호 줄이기
            page_no -= 1

    def parse_date(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")  # 날짜 포맷에 맞게 조정
        except ValueError:
            return datetime.datetime.min  # 날짜 형식이 잘못된 경우 최소 날짜로 설정

    descriptions_list.sort(key=lambda desc: parse_date(desc.creation_date), reverse=True)

    # 결과 반환
    return descriptions_list

"""

import requests

def calculate_distance_openrouteservice(api_key, coordinates):
    
    #OpenRouteService API를 사용하여 두 지점 간 거리 계산
    #:param api_key: OpenRouteService API 키
    #:param coordinates: 경로 좌표 [[lon1, lat1], [lon2, lat2]]
    #:return: 거리 (미터 단위) 또는 오류 메시지


    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": coordinates  # [[lon1, lat1], [lon2, lat2]]
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        result = response.json()
        try:
            distance = result['routes'][0]['summary']['distance']  # 미터 단위
            return distance
        except (KeyError, IndexError):
            return "응답 데이터에 예상된 필드가 없습니다."
    else:
        # 디버깅 로그 출력
        print(f"API 호출 실패: {response.status_code}, {response.text}")
        return None

# 사용 예제
if __name__ == "__main__":
    coordinates = [[126.9780, 37.5665], [126.9895, 37.5651]]  # [경도, 위도]
    api_key = "5b3ce3597851110001cf62480d4bea18319941a5a72e6e7b45e3be19"  # OpenRouteService API 키
    distance = calculate_distance_openrouteservice(api_key, coordinates)
    if distance:
        print(f"두 지점 간 거리: {distance / 1000:.2f} km")
    else:
        print("거리를 계산할 수 없습니다.")

def test_openrouteservice(api_key):
    url = "https://api.openrouteservice.org/ping"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    return response.status_code == 200

api_key = "5b3ce3597851110001cf62480d4bea18319941a5a72e6e7b45e3be19"
if test_openrouteservice(api_key):
    print("API 키가 유효합니다.")
else:
    print("API 키가 유효하지 않거나 차단되었습니다.")


"""
if __name__ == "__main__":
    app.run(debug=False)

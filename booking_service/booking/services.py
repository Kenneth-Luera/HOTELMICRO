import requests

HOTEL_SERVICE_URL = "http://127.0.0.1:8001/api/rooms/"

def get_room(room_id):

    try:
        response = requests.get(
            f"{HOTEL_SERVICE_URL}{room_id}/internal/",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        print("ERROR STATUS:", response.status_code)
        return None

    except requests.RequestException as e:
        print("ERROR REQUEST:", e)
        return None
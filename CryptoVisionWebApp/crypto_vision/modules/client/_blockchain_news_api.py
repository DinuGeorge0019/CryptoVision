
import requests


def get_blockchain_news():
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": "pub_366241f18495e4fb9ea729e201e084e244f40",
        "q": "bitcoin",
        "country": "us",
        "language": "en",
        "category": "top"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response = response.json()
        return response['results']
    else:
        return None
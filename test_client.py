import concurrent.futures

import requests


def send_queries(endpoints):
    
    def send_query(endpoint):
        response = requests.get(endpoint)
        print(f"Query {endpoint}: {response.status_code}, {response.json()}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_query, endpoint) for endpoint in endpoints]
        concurrent.futures.wait(futures)

profiles = ('cristiano', 'leomessi', 'selenagomez')
endpoints = [f"http://0.0.0.0:5000/getPhotos/?username={profile}&max_count=20" for profile in profiles]
send_queries(endpoints)

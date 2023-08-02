import concurrent.futures

import requests


def send_queries(endpoint, num_queries):
    def send_query(query_num):
        response = requests.get(endpoint)
        print(f"Query {query_num}: {response.status_code}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_query, i + 1) for i in range(num_queries)]
        concurrent.futures.wait(futures)


endpoint = "http://127.0.0.1:8000/getPhotos/?username=modestmouse"
num_queries = 5
send_queries(endpoint, num_queries)

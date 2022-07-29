from extra_common_words import Extra_common_words_summarization

import json
import requests as rq

url = 'https://kinopoiskapiunofficial.tech'


def load_film(session, id):
    uid_api_url = f'/api/v2.2/films/{id}/reviews'
    exploring_response = session.get(url + uid_api_url)
    exploring_resp_text = json.loads(exploring_response.text)

    pages = range(1, exploring_resp_text['totalPages'])
    reviews = []
    for page in pages:
        params = {'page': page}
        response = session.get(url + uid_api_url, params=params)
        full_data = json.loads(response.text)
        for item in full_data['items']:
            reviews.append(item['description'])
    return reviews

my_session = rq.Session()
headers = {
    'X-API-KEY': '77b33ccc-8651-4a76-9a56-c48a4bb873a1',
}
my_session.headers.update(headers)

reviews = load_film(my_session, 105948)
summarizer = Extra_common_words_summarization()
token_len = 100
extras = []

for review in reviews:
    summarized_review = summarizer.summarize(review, summary_fraction=0.00, language='russian')
    print(summarized_review)
    if len(summarized_review) < token_len:
        print('Учтем это представления для тэггинга!')
        extras.append(summarized_review)
    else:
        print('Представление слишком длинное')
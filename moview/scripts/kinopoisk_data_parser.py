from extra_common_words import Extra_common_words_summarization

import json
import requests as rq
import os


url = os.environ['API_URL']
token = os.environ['API_TOKEN']

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

def get_taggs_summarization(session, id, token_bound=100, review_bound=None, summary_fraction=0.0, final_fraction=0.2):
    reviews = load_film(session, id)
    if review_bound is None:
        review_bound = len(reviews)
    reviews = reviews[:review_bound]
    
    summarizer = Extra_common_words_summarization()
    extras = []

    for review in reviews:
        summarized_review = summarizer.summarize(review, summary_fraction=summary_fraction, language='russian')
        if len(summarized_review) < token_bound:
            extras.append(summarized_review)

    extra_review = '. '.join(extras)
    summarized_extra = summarizer.summarize(extra_review, summary_fraction=final_fraction, language='russian')
    return summarized_extra


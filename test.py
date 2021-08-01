import unittest
import requests
import sys
import json


class TestFluentdIntegration(unittest.TestCase):
    logzio_type = None
    api_token = None
    def test_integration(self):
        logzio_type = self.logzio_type
        query = f'type:{logzio_type}'
        api_url = 'https://api.logz.io/v1/search'
        api_token = self.api_token
        headers = {
            'X-API-TOKEN': api_token,
            'Content-Type': 'application/json'
        }
        api_query = {
            "query": {
                "bool": {
                    "must": [{
                        "query_string": {
                            "query": query
                        }
                    },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-10m",
                                    "lte": "now"
                                }
                            }
                        }
                    ]
                }
            },
            "size": 50,
            "from": 0
        }
        response = requests.post(url=api_url, json=api_query, headers=headers)
        log_count = int(json.loads(response.text)['hits']['total'])
        print(f'api_token: {api_token}')
        print(f'Query: {query}')
        print(response.request.body)
        valid_count = 50
        self.assertEqual(log_count, valid_count, f"Should be {valid_count}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestFluentdIntegration.logzio_type = sys.argv.pop()
        TestFluentdIntegration.api_token = sys.argv.pop()
unittest.main()

import requests


class SCAPI:

    def __init__(self):
        self.api_url = 'https://csapi.singlecare.com/services/v1_0/private/CRMService.svc/'

    def post(self, service, params):
        headers = {'Content-Type': 'application/json'}
        try:
            return requests.request('POST', self.api_url + service, headers=headers, json=params)
        except Exception as e:
            print(e)

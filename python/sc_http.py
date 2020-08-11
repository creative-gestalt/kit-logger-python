import requests as req


class SCHTTP:

    def __init__(self):
        self.base_url = 'https://crm.singlecare.com/Account/Login?ReturnUrl=%2F'

    def get(self, params, headers):
        try:
            return req.request('GET', self.base_url, headers=headers, data=params)
        except Exception as e:
            print(e)

    def post(self, params, headers):
        try:
            return req.request('POST', self.base_url, headers=headers, data=params)
        except Exception as e:
            print(e)

from python.sc_http import SCHTTP
from python.sc_api import SCAPI
from bs4 import BeautifulSoup
import urllib.parse as parse
from python import logger
import json

api = SCAPI()
http = SCHTTP()
print = logger.print_and_log


def get_authenticated(self):
    """Requests `GET` then `POST` to obtain sales rep id and auth token
       :returns user_id, api_token
    """
    # Request to obtain cookie and hidden token
    headers_1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'connection': 'keep-alive',
        'dnt': '1',
        'host': 'crm.singlecare.com',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Android 10; Mobile; rv:81.0) Gecko/81.0 Firefox/81.0'
    }
    response_1 = http.get(params={}, headers=headers_1)
    soup = BeautifulSoup(response_1.content, 'lxml')
    cookie = str(response_1.cookies.get_dict()['__RequestVerificationToken'])
    token = str(soup.input['value'])
    encoded_email = parse.quote_plus(self.email)

    # Request to obtain SalesRepAPICookie
    params = f'__RequestVerificationToken={token}&Email={encoded_email}&Password={self.password}'
    headers_2 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'connection': 'keep-alive',
        'content-length': '169',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'__RequestVerificationToken={cookie}',
        'dnt': '1',
        'host': 'crm.singlecare.com',
        'origin': 'https://crm.singlecare.com',
        'referer': 'https://crm.singlecare.com/Account/Login?ReturnUrl=%2F',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Android 10; Mobile; rv:81.0) Gecko/81.0 Firefox/81.0'
    }
    response_2 = http.post(params=params, headers=headers_2)
    (user_id, api_token) = str(response_2.history[0].cookies.get_dict()['SalesRepAPICookie']).split('!')
    return user_id, api_token


def retrieve_locations(self, user_id, api_token):
    """Sends `POST` to CRM API to acquire providers in a given zip code
       :returns filtered location_ids
    """
    params = {
        'Value': {
            'PostalCode': self.zip_code,
            'PageSize': '500'
        },
        'Authentication': {
            'ApiToken': api_token,
            'UserId': user_id
        }
    }
    response = api.post(service='SearchPractices', params=params)
    return filter_response(self, json.loads(response.content))


def filter_response(self, data):
    """Filters locations by 3 criteria:
          not in used_location_id,
             LocationStatusTypeId exists and is equal to 1,
             OR
             LocationStatusType has no value and SalesRepId is equal to 0
       :returns location_ids
    """
    location_ids = []
    used_location_ids = []
    with open('data/used/used_location_ids.txt', 'r') as f:
        for row in f:
            used_location_ids.append(row.rstrip())
    count = len(data['List'])
    # Filters out pending, do not pursue, and what ids we've used already
    for index, _ in enumerate(range(count)):
        if not used_location_ids.__contains__(str(data['List'][index]['Location']['LocationId']).strip()):
            if data['List'][index]['LocationStatusType'] is not None:
                if data['List'][index]['LocationStatusType']['LocationStatusTypeId'] == 1:
                    location_ids.append(data['List'][index]['Location']['LocationId'])
            # Filters out locations with reps on them if LocationStatusType is null
            elif data['List'][index]['LocationStatusType'] is None and data['List'][index]['SalesRepId'] == 0:
                location_ids.append(data['List'][index]['Location']['LocationId'])
    if len(location_ids) == 0:
        remove_location(self)
        return []
    else:
        return location_ids[:self.iterations]


def remove_location(self):
    """Removes zip code from master list"""
    with open(f'states/{self.state}/city-dictionary.txt', 'r') as r:
        zip_list = r.readlines()
    item_index = (i for i, e in zip_list if e.__contains__(self.zip_code))
    del zip_list[next(item_index)]
    with open(f'states/{self.state}/city-dictionary.txt', 'w') as w:
        w.write('\n'.join(zip_list))
    print(f'Location {self.zip_code} was removed')


def send_drop_off(location_id, member, group, user_id, api_token):
    """Sends `POST` api request to LogDropOffKit service
       :returns success, error
    """
    params = {
        'LocationId': location_id,
        'MemberNumber': sanitize(member),
        'GroupNumber': sanitize(group),
        'Authentication': {
            'ApiToken': api_token,
            'UserId': user_id
        }
    }
    response = api.post(service='LogDropOffKit', params=params)
    parsed = json.loads(response.content)
    error = parsed['Errors']
    success = parsed['Success']
    if not success:
        print(error)
    return success, error


def sanitize(string):
    if str(string).__contains__('\n'):
        return string.strip()
    else:
        return str(string)


import requests, time, json, os
from bs4 import BeautifulSoup
from random import randint

userSession = requests.Session()
userSession.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
})

# need to watch any changes
paramsLogin = {
    'authenticity_token': '',
    'session[email]': '',
    'session[password]': ''
}

csrfHeaders = {
    'X-CSRF-Token': '',
    'X-Requested-With': 'XMLHttpRequest'
}

def requestWebPage(method, url, data = {}, headers = {}, checkStatusCode = True):
    global userSession
    while True:
        try:
            response = userSession.request(method, url, data = data, headers = headers, timeout = 5)
        except requests.exceptions.RequestException:
            print "timeout"
            time.sleep(5)
            continue
        if checkStatusCode and response.status_code != 200:
            print "error page"
            time.sleep(5)
            continue
        return response

loginPage = requestWebPage('GET', 'https://500px.com/login')
time.sleep(3)

loginPage_soup = BeautifulSoup(loginPage.text, 'html.parser')
paramsLogin['authenticity_token'] = loginPage_soup.find('meta', {'name': 'csrf-token'}).get('content')
csrfHeaders['X-CSRF-Token'] = paramsLogin['authenticity_token']

userLogin = requestWebPage('POST', 'https://api.500px.com/v1/session', data = paramsLogin)

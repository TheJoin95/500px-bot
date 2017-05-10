import sys
import getopt
import requests
import time, json, os
from bs4 import BeautifulSoup
from random import randint

def getJsonFile(filename):
    fileContent = []
    if filename != '':
        f = open(filename)
        try:
            fileContent = json.load(f)
            pass
        except Exception, e:
            print e
            print 'error: filename - invalid json'
            pass
        
        f.close()

    return fileContent

def makeRequest(method, url, data = {}, headers = {}, checkStatusCode = True, proxies = None):
    global userSession
    try:
        response = userSession.request(method, url, data = data, headers = headers, proxies = None, timeout = 5)
    except requests.exceptions.RequestException:
        print "timeout"
        time.sleep(5)
        continue
    if checkStatusCode and response.status_code != 200:
        print "error page"
        time.sleep(5)
        continue
    return response

def doLogin():
    global userSession, configValues

    loginPage = makeRequest('GET', 'https://500px.com/login')
    time.sleep(3)

    loginPage_bs = BeautifulSoup(loginPage.text, 'html.parser')
    configValues['paramsLogin']['authenticity_token'] = loginPage_bs.find('meta', {'name': 'csrf-token'}).get('content')
    csrfHeaders['X-CSRF-Token'] = configValues['paramsLogin']['authenticity_token']

    userLogin = makeRequest('POST', 'https://api.500px.com/v1/session', data = configValues['paramsLogin'])
    responseLoginPost = json.loads(userLogin.content)
    return (responseLoginPost['success'] == True and responseLoginPost['success'])


if __name__ == '__main__':

    argv = sys.argv[1:]
    configFile = None
    userSession = requests.Session()
    userSession.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    })

    # need to watch any changes
    configValues = {
        "paramsLogin": {
            'authenticity_token': '',
            'session[email]': '',
            'session[password]': ''
        }
    }

    csrfHeaders = {
        'X-CSRF-Token': '',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        opts, args = getopt.getopt(argv,"h:u:p:c:i",["user=","password=", "config="])
    except getopt.GetoptError:
        print 'run.py -u <email> -p <password> -c <config>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'run.py -u <user> -p <password> -c <filename config>'
            sys.exit()
        elif opt in ("-u", "--user"):
            configValues["paramsLogin"]["session[email]"] = arg
        elif opt in ("-p", "--password"):
            configValues["paramsLogin"]["session[password]"] = arg
        elif opt in ("-c", "--config"):
            configFile = arg

    print configFile
    if configFile != None:
        configValues = getJsonFile(configFile)
    
    if "paramsLogin" not in configValues:
        raise "error: undefined paramsLogin in config"

    doLogin()
import sys
import getopt
import requests
import time, json, os
from bs4 import BeautifulSoup
from random import randint

DOMAIN = "https://500px.com"
API_DOMAIN = "https://api.500px.com/v1"
API_ENDPOINT_UNFOLLOW = "unfollow"
API_ENDPOINT_LOGOUT = "logout"

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
        pass
    if checkStatusCode and response.status_code != 200:
        print "error page"
        time.sleep(5)
        pass
    return response

def updateCSRFHeaders():
    global userSession, configValues
    # get page and check for change of token

def doLogin():
    global userSession, configValues

    loginPage = makeRequest('GET', DOMAIN + '/login')
    time.sleep(3)

    loginPage_bs = BeautifulSoup(loginPage.text, 'html.parser')
    configValues['paramsLogin']['authenticity_token'] = loginPage_bs.find('meta', {'name': 'csrf-token'}).get('content')
    configValues["csrfHeaders"]['X-CSRF-Token'] = configValues['paramsLogin']['authenticity_token']

    userLogin = makeRequest('POST', API_DOMAIN + '/session', data = configValues['paramsLogin'])
    responseLoginPost = json.loads(userLogin.content)
    configValues["user_data"] = responseLoginPost["user"]

    return (responseLoginPost['success'] == True and responseLoginPost['success'])

def doLogout():
    global userSession, configValues

    # need to get back, from the last request, the "authenticity_token" of logout's form

    logoutParams = {
        "_method": "delete",
        "authenticity_token": configValues["csrfHeaders"]['X-CSRF-Token']
    }

    logoutPage = makeRequest("POST", DOMAIN+"/" + API_ENDPOINT_LOGOUT, data = logoutParams)
    print logoutPage.status_code

def unFollow(username, timeout = 5):
    global userSession, configValues
    # https://500px.com/{username}/unfollow POST
    print "unfollow"
    try:
        unfollowResp = userSession.post(DOMAIN + '/' + username + '/' + API_ENDPOINT_UNFOLLOW, timeout = timeout, headers = configValues["csrfHeaders"])
        if unfollowResp.status_code == 200:
            print 'Unfollowed ' + username
        elif unfollowResp.status_code == 404:
            print "404 - user not exists"
        else:
            print unfollowResp.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(5)

def doFollow(username):
    # https://500px.com/{username}/follow POST
    global userSession, configValues

    try:
        follow = userSession.post(API_DOMAIN + '/' + username + '/follow', headers = configValues["csrfHeaders"])
        if follow.status_code == 200:
            print "Following " + username
        elif follow.status_code == 404:
            print username + " not exists"
        else
            print follow.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(3)

def vote(idphoto):
    # https://api.500px.com/v1/photos/{idphoto}/vote?vote=1 POST
    global userSession, configValues
    # https://500px.com/{username}/unfollow POST
    print "vote"
    try:
        vote = userSession.post(API_DOMAIN + '/photos/' + idphoto + '/vote?vote=1', headers = configValues["csrfHeaders"])
        if vote.status_code == 200:
            print 'Voted for ' + idphoto
        elif vote.status_code == 404:
            print "404 - photo not exists"
        else:
            print vote.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(5)

def unVote(idphoto):
    # https://api.500px.com/v1/photos/{idphoto}/vote DELETE
    global userSession, configValues
    # https://500px.com/{username}/unfollow POST
    print "unVote"
    try:
        vote = userSession.delete(API_DOMAIN + '/photos/' + idphoto + '/vote', headers = configValues["csrfHeaders"])
        if vote.status_code == 200:
            print 'Unvoted for ' + idphoto
        elif vote.status_code == 404:
            print "404 - photo not exists"
        else:
            print vote.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(5)

def getLikesOfPhoto(idphoto, page=0):
    # https://api.500px.com/v1/photos/{idphoto}/votes?include_following=true&page=2&rpp=8 GET
    global userSession, configValues

    try:
        votes = userSession.get(API_DOMAIN + '/photos/' + idphoto + '/votes?include_following=true&page='+page+'&rpp=8', headers = configValues["csrfHeaders"])
        if votes.status_code == 200:
            print 'Unvoted for ' + idphoto
        elif votes.status_code == 404:
            print "404 - photo not exists"
        else:
            print votes.status_code

        pass
    except Exception, e:
        print e
        pass

    return votes

def doComment():
    # https://api.500px.com/v1/photos/211674051/comments?sort=created_at&include_subscription=1&include_flagged=1&nested=1 POST
    # payload JSON, need to GET all profile data :S
    # {"body":"Really nice shot! love the combination and the colors :)","user":{"id":6775294,"username":"mikistorm","firstname":"Miki","lastname":"Lombardi","fullname":"Miki Lombardi","affection":1310,"userpic_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","userpic_https_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","cover_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/cover_2048.jpg?4","upgrade_status":0,"usertype":0,"city":"Firenze","state":"","country":"Italy","admin":false,"avatars":{"default":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1"},"large":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/2.jpg?1"},"small":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/3.jpg?1"},"tiny":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/4.jpg?1"}},"show_groups_onboarding":false,"followers_count":11,"photos_count":131,"views_count":19225,"followees_count":98,"email":"mikistorm@live.it","upload_limit":20,"store_enabled":true,"show_nude":false,"registration_date":"2014-02-03T04:21:46-05:00","birthday":"1995-06-15","upgrade_expiry_date":"2015-06-23","avatar_version":1,"needs_contact_verification":false,"buyer":false,"photo_availability_filter":1},"replies":[]}
    print "docomment"

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
        },
        "csrfHeaders": {
            'X-CSRF-Token': '',
            'X-Requested-With': 'XMLHttpRequest'
        }
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

    print doLogin()
    print unFollow("username")
    # print doLogout()
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

TO_FOLLOW_FILE = "tofollow.json"
FOLLOWED_FILE = "follow.json"
COMMENT_LOOKUP_FILE = "comment.json"

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

def appendToFile(data, filename="test.json"):
    feeds = []
    with open(filename, mode='r+') as feedsjson:
        feeds = json.load(feedsjson)

    with open(filename, mode='w') as feedsjson:
        if type(data) == type([]):
            feeds = data
        else:
            feeds.append(data)
        
        feeds = list(set(feeds))
        json.dump(feeds, feedsjson)

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

    responseLoginPost = False
    if "paramsLogin" in configValues:
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
            appendToFile(username, FOLLOWED_FILE)
        elif follow.status_code == 404:
            print username + " not exists"
        else:
            print follow.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(3)

def checkAlreadyVoted(idphoto=''):
    global userSession, configValues
    
    response = False
    page = 1

    while 1:
        votes = getLikesOfPhoto(idphoto=idphoto, page=page)
        if "users" in votes and len(votes["users"]) > 0:
            for vote in votes["users"]:
                if(vote["id"] == configValues["user_data"]["id"]):
                    response = True
                    break
        else:
            break

        if(response == True):
            break
        else:
            page = page + 1

    print "checking already votes: " + str(response)
    return response

def vote(el):
    # https://api.500px.com/v1/photos/{idphoto}/vote?vote=1 POST
    global userSession, configValues
    
    idphoto = ""
    response = False
    
    # add check of configValues and increment count per day
    if ("voted" not in el or el["voted"] == False):
        idphoto = str(el['id'])
    elif (not checkAlreadyVoted(el["id"])):
        idphoto = str(el['id'])
    else:
        return False;

    try:
        vote = userSession.post(API_DOMAIN + '/photos/' + idphoto + '/vote?vote=1', headers = configValues["csrfHeaders"])
        if vote.status_code == 200:
            print 'Voted for ' + idphoto
            response = True
        elif vote.status_code == 404:
            print "404 - photo not exists"
        else:
            print vote.status_code

        pass
    except Exception, e:
        print "exception vote: " + str(e)
        pass

    time.sleep(5)
    return response

def unVote(idphoto):
    # https://api.500px.com/v1/photos/{idphoto}/vote DELETE
    global userSession, configValues

    response = False
    try:
        vote = userSession.delete(API_DOMAIN + '/photos/' + str(idphoto) + '/vote', headers = configValues["csrfHeaders"])
        if vote.status_code == 200:
            print 'Unvoted for ' + idphoto
            response = True
        elif vote.status_code == 404:
            print "404 - photo not exists"
        else:
            print vote.status_code

        pass
    except Exception, e:
        print "exception unvote: " + str(e)
        pass

    time.sleep(5)
    return response

def getLikesOfPhoto(idphoto, page=0):
    # https://api.500px.com/v1/photos/{idphoto}/votes?include_following=true&page=2&rpp=8 GET
    global userSession, configValues
    votes = []
    try:
        votes = userSession.get(API_DOMAIN + '/photos/' + str(idphoto) + '/votes?include_following=true&page='+str(page)+'&rpp=8', headers = configValues["csrfHeaders"])
        if votes.status_code == 200:
            print 'getlikes for ' + str(idphoto)
            votes = json.loads(votes.text)
        elif votes.status_code == 404:
            print "404 - photo not exists"
        else:
            print votes.status_code

        pass
    except Exception, e:
        print "exception getlikes: " + str(e)
        pass

    return votes

def search(term="",typeSearch="photos",sort="",categories=[], exclude_nude=True, page=1):
    # endpoin GET https://api.500px.com/v1/photos/search
    # params
    # type:photos
    # term:london
    # sort:highest_rating|pulse|created_at default: revelance
    # only:Aerial|Animals,Celebrities multiple
    # image_size[]:1
    # image_size[]:2
    # image_size[]:32
    # image_size[]:31
    # image_size[]:33
    # image_size[]:34
    # image_size[]:35
    # image_size[]:36
    # image_size[]:2048
    # image_size[]:4
    # image_size[]:14
    # include_states:true
    # formats:jpeg,lytro
    # include_tags:true
    # exclude_nude:true
    # page:1
    # rpp:50
    global userSession, configValues

    params = {
        "term": term,
        "type": typeSearch,
        "image_size": [1,2,32,31,33,34,35,36,2048,4,14],
        "include_states": True,
        "formats": "jpeg,lytro",
        "exclude_nude": exclude_nude,
        "page": page,
        "rpp": 50
    }

    if sort != "":
        params["sort"] = sort

    if categories != "":
        params["only"] = ",".join(categories) #working?


    search = []
    try:
        search = userSession.get(API_DOMAIN + '/photos/search', params=params, headers = configValues["csrfHeaders"])
        if search.status_code == 200:
            search = json.loads(search.text)
        elif search.status_code == 404:
            print "404 - photo not exists"
        else:
            print search.status_code

        pass
    except Exception, e:
        print "exception search: " + str(e)
        pass

    return search

def getComment(idphoto="", sort="created_at", include_subscription=1,include_flagged=1, nested=1,page=1):
    global userSession, configValues
    # https://api.500px.com/v1/photos/388736/comments?sort=created_at&include_subscription=1&include_flagged=1&nested=1&page=1&rpp=30
    params = {
        "sort": sort,
        "include_subscription": include_subscription,
        "include_flagged": include_flagged,
        "nested": nested,
        "page": page,
        "rpp": 30
    }

    comments = []
    try:
        comments = userSession.get(API_DOMAIN + '/photos/' + str(idphoto) + '/comments', params=params, headers = configValues["csrfHeaders"])
        if comments.status_code == 200:
            comments = json.loads(comments.text)
        elif comments.status_code == 404:
            print "404 - photo not exists"
        else:
            print comments.status_code

        pass
    except Exception, e:
        print "exception getComment: " + str(e)
        pass

    return comments

def doComment(idphoto="", body="Great work!", auto=False):
    global userSession, configValues
    # se il commento non e gia stato fatto, fallo
    # https://api.500px.com/v1/photos/211674051/comments?sort=created_at&include_subscription=1&include_flagged=1&nested=1 POST
    # payload JSON, need to GET all profile data :S
    # {"body":"Really nice shot! love the combination and the colors :)","user":{"id":6775294,"username":"mikistorm","firstname":"Miki","lastname":"Lombardi","fullname":"Miki Lombardi","affection":1310,"userpic_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","userpic_https_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","cover_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/cover_2048.jpg?4","upgrade_status":0,"usertype":0,"city":"Firenze","state":"","country":"Italy","admin":false,"avatars":{"default":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1"},"large":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/2.jpg?1"},"small":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/3.jpg?1"},"tiny":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/4.jpg?1"}},"show_groups_onboarding":false,"followers_count":11,"photos_count":131,"views_count":19225,"followees_count":98,"email":"mikistorm@live.it","upload_limit":20,"store_enabled":true,"show_nude":false,"registration_date":"2014-02-03T04:21:46-05:00","birthday":"1995-06-15","upgrade_expiry_date":"2015-06-23","avatar_version":1,"needs_contact_verification":false,"buyer":false,"photo_availability_filter":1},"replies":[]}
    data = {
        "body": body,
        "user": configValues["user_data"]
    }

    comment = False
    try:
        comment = userSession.post(API_DOMAIN + '/photos/' + str(idphoto) + '/comments', data=data, headers = configValues["csrfHeaders"])
        if comment.status_code == 200:
            print "comment done"
            comment = True
        elif comment.status_code == 404:
            print "404 - photo not exists"
        else:
            print comment.status_code

        pass
    except Exception, e:
        print "exception doComment: " + str(e)
        pass

    time.sleep(5)
    return comment

def checkAlreadyComment(idphoto=''):
    global userSession, configValues

    response = False
    page = 1

    while 1:
        comments = getComment(idphoto=idphoto, page=page)
        if "comments" in comments and len(comments["comments"]) > 0:
            for comment in comments["comments"]:
                if(comment["user_id"] == configValues["user_data"]["id"]):
                    response = True
                    break
        else:
            break

        if(response == True):
            break
        else:
            page = page + 1

    print "checking already comment: " + str(response)
    return response

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


    print "Trying to get a config by file"
    if configFile != None:
        configValues = getJsonFile(configFile)
    else:
        print "Warning: no config file was found"
    
    if "paramsLogin" not in configValues or type(configValues) == type(False):
        raise ValueError("ERROR: undefined paramsLogin in config")

    print "Logggin in"
    resultLogin = doLogin()

    print "Logged in: " + str(resultLogin)

    if resultLogin == False:
        raise ValueError('Check your login data; login failed')
    
    londonSearch = search("london")
    # print londonSearch

    for el in londonSearch["photos"]:
        # need to add to db or in a queue
        #print "need to check criteria"
        print "processing: " + str(el["id"])
        print "vote: " + str(vote(el))
        # print "need to check if not commented + criteria"
        willDoComment = False
        if(not checkAlreadyComment(el["id"]) and ("comment" in configValues and configValues["comment"] == True)):
            print "comment: " + str(doComment(idphoto=el["id"], auto=True))
            willDoComment = True

        if(willDoComment):
            print "waiting 30"
            time.sleep(30)
        # print "add to vote, follow user and comment"
        # print "need to check if not follow + criteria"
        # print "need to check likes and follow tags + users"

    #doComment("81367687")
    # print getLikesOfPhoto("81367687")
    #vote("81367687")
    # print doLogout()
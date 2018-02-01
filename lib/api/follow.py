def unFollow(username, timeout = 5):
    global userSession, configValues
    # https://500px.com/{username}/unfollow POST
    print "unfollow"
    response = False
    try:
        unfollowResp = userSession.post(DOMAIN + '/' + username + '/' + API_ENDPOINT_UNFOLLOW, timeout = timeout, headers = configValues["csrfHeaders"])
        if unfollowResp.status_code == 200:
            print 'Unfollowed ' + username
            response = True
            updateStats("unfollowingCounter")
        elif unfollowResp.status_code == 404:
            print "404 - user not exists"
        else:
            print unfollowResp.status_code

        pass
    except Exception, e:
        print e
        pass

    time.sleep(5)
    return response

def doFollow(username):
    # https://500px.com/{username}/follow POST
    global userSession, configValues
    response = False
    try:
        follow = userSession.post(API_DOMAIN + '/' + username + '/follow', headers = configValues["csrfHeaders"])
        if follow.status_code == 200:
            print "Following " + username
            updateStats("followingCounter")
            response = True
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
    return response

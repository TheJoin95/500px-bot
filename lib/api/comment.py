from random import randint

def getComment(self, idphoto="", sort="created_at", include_subscription=1,include_flagged=1, nested=1,page=1):
    """https://api.500px.com/v1/photos/388736/comments?sort=created_at&include_subscription=1&include_flagged=1&nested=1&page=1&rpp=30"""
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
        comments = self.enviroment_variables["userSession"].get(self.constants["API_DOMAIN"] + '/photos/' + str(idphoto) + '/comments', params=params, headers = self.enviroment_variables["configValues"]["csrfHeaders"])
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

def doComment(self, idphoto="", body="Great work!", auto=False):
    # se il commento non e gia stato fatto, fallo
    # https://api.500px.com/v1/photos/211674051/comments?sort=created_at&include_subscription=1&include_flagged=1&nested=1 POST
    # payload JSON, need to GET all profile data :S
    # {"body":"Really nice shot! love the combination and the colors :)","user":{"id":6775294,"username":"username","firstname":"Miki","lastname":"Lombardi","fullname":"Miki Lombardi","affection":1310,"userpic_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","userpic_https_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1","cover_url":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/cover_2048.jpg?4","upgrade_status":0,"usertype":0,"city":"Firenze","state":"","country":"Italy","admin":false,"avatars":{"default":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/1.jpg?1"},"large":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/2.jpg?1"},"small":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/3.jpg?1"},"tiny":{"https":"https://pacdn.500px.org/6775294/2b0940d604a671bd4a8ddb2d8ee2c81920d13d75/4.jpg?1"}},"show_groups_onboarding":false,"followers_count":11,"photos_count":131,"views_count":19225,"followees_count":98,"email":"email@email.it","upload_limit":20,"store_enabled":true,"show_nude":false,"registration_date":"2014-02-03T04:21:46-05:00","birthday":"1995-06-15","upgrade_expiry_date":"2015-06-23","avatar_version":1,"needs_contact_verification":false,"buyer":false,"photo_availability_filter":1},"replies":[]}
    data = {
        "body": body,
        "user": self.enviroment_variables["configValues"]["user_data"]
    }

    comment = False
    if not checkAlreadyComment(self, idphoto):
        try:
            comment = self.enviroment_variables["userSession"].post(self.constants["API_DOMAIN"] + '/photos/' + str(idphoto) + '/comments', data=data, headers = self.enviroment_variables["configValues"]["csrfHeaders"])
            if comment.status_code == 200:
                print "comment done"
                updateStats("commentCounter")
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

def checkAlreadyComment(self, idphoto=''):
    response = False
    page = 1

    while 1:
        comments = getComment(idphoto=idphoto, page=page)
        if "comments" in comments and len(comments["comments"]) > 0:
            for comment in comments["comments"]:
                if(comment["user_id"] == self.enviroment_variables["configValues"]["user_data"]["id"]):
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

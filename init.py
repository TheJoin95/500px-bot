import sys
import getopt
import datetime
import time, json, os
from random import randint
import atexit

from lib import utils
from lib.bot import Bot

def updateStats(key=""):
    today = datetime.datetime.today().strftime('%Y%m%d')

    if today in STATS[key]:
        STATS[key][today]["count"] = STATS[key][today]["count"] + 1
    else:
        STATS[key][today].append({"count": 1})

    STATS[key]["last_update"] = datetime.datetime.now()

    return True

def checkCriteria(key="", content={}):
    global BASE_CONFIG, configValues
    response = False
    
    criteriaKey = {
        "searchParams": ["search_page_limit"],
        "paramsLike": ["max_likes_per_day", "max_likes_to_like", "min_likes_to_like"],
        "paramsUnLike": ["max_unlikes_per_day"],
        "paramsFollow": ["max_follows_per_day", "max_followers_to_follow", "min_followers_to_follow", "max_following_to_follow", "min_following_to_follow", "max_followers_to_following_ratio", "max_following_to_followers_ratio"],
        "paramsUnFollow": ["max_unfollows_per_day", ],
        "paramsComment": ["max_comments_per_day"]
    }

    # mapping key of stats for criteriaKey
    statsKey = {
        "paramsLike" : "voteCounter",
        "paramsUnLike" : "unvoteCounter",
        "paramsFollow" : "followingCounter",
        "paramsUnFollow" : "unfollowingCounter",
        "paramsComment" : "commentCounter"
    }

    # maybe i need to use jsonLogin here for return a boolean
    if key in criteriaKey:
        for value in criteriaKey[key]:
            # need to check the values by condition
            response = True

    return response

def updateCSRFHeaders():
    global userSession, configValues
    # get page and check for change of token
    
def store_all_and_logout(botClass):
    botClass.store_queue()
    botClass.logout()

if __name__ == '__main__':

    argv = sys.argv[1:]

    mainBot = Bot()

    mainBot.addEnviromentVariable(key="configFile", value=None)
    mainBot.addEnviromentVariable(key="userSession", value=requests.Session())
    mainBot.addEnviromentVariable(key="configValues", value={
        "paramsLogin": {
            'authenticity_token': '',
            'session[email]': '',
            'session[password]': ''
        },
        "csrfHeaders": {
            'X-CSRF-Token': '',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })

    mainBot.enviroment_variables["userSession"].headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    })

    try:
        opts, args = getopt.getopt(argv,"h:u:p:c:i",["user=","password=", "config="])
    except getopt.GetoptError:
        print 'init.py -u <email> -p <password> -c <config>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'run.py -u <user> -p <password> -c <filename config>'
            sys.exit()
        elif opt in ("-u", "--user"):
            mainBot.enviroment_variables["configValues"]["paramsLogin"]["session[email]"] = arg
        elif opt in ("-p", "--password"):
            mainBot.enviroment_variables["configValues"]["paramsLogin"]["session[password]"] = arg
        elif opt in ("-c", "--config"):
            mainBot.enviroment_variables["configFile"] = arg


    if mainBot.enviroment_variables["configFile"] != None:
        mainBot.enviroment_variables["configValues"] = utils.getJsonFile(mainBot.enviroment_variables["configFile"])
    else:
        print "Warning: no config file was found"
    
    if "paramsLogin" not in mainBot.enviroment_variables["configValues"] or type(mainBot.enviroment_variables["configValues"]) == type(False):
        raise ValueError("ERROR: undefined paramsLogin in config")

    resultLogin = mainBot.login()
    if resultLogin == False:
        raise ValueError('Check your login data; login failed')

    # search and more actions inside (just for now, only vote)
    mainBot.search("aquila")
    mainBot.search("gran sasso")
    
    mainBot.logout()

    atexit.register(store_all_and_logout, mainBot)
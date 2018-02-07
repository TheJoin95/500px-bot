import time
import json
from bs4 import BeautifulSoup
from Queue import *
from threading import Thread

from ..utils import *
from ..api import API

class Bot(API):
    """
    Class Bot is a 500px bot
    """
    def __init__(self):
        super(Bot, self).__init__()
        self.constants = {}
        self.enviroment_variables = {}
        self.populateBase()

    def addConstant(self, key="", value=""):
        returnValue = False
        if key != "" and value != "":
            self.constants[key] = value
            returnValue = True
        return returnValue

    def removeConstant(self, key=""):
        returnValue = False
        if key != "" and value != "":
            del self.constants[key]
            returnValue = True
        return returnValue
    
    def addEnviromentVariable(self, key="", value=""):
        returnValue = False
        if key != "" and value != "":
            self.enviroment_variables[key] = value
            returnValue = True
        return returnValue

    def removeEnviromentVariable(self, key=""):
        returnValue = False
        if key != "" and value != "":
            del self.enviroment_variables[key]
            returnValue = True
        return returnValue

    def populateBase(self):
        self.constants["DOMAIN"] = "https://500px.com"
        self.constants["API_DOMAIN"] = "https://api.500px.com/v1"
        self.constants["API_ENDPOINT_UNFOLLOW"] = "unfollow"
        self.constants["API_ENDPOINT_LOGOUT"] = "logout"

        self.constants["WORKER_THREADS"] = 3 # definire max worker per queue
        self.constants["MAX_WORKER_SEARCH"] = 10
        self.constants["QUEUE_SEARCH"] = Queue()
        self.constants["QUEUE_VOTE"] = Queue()
        self.constants["QUEUE_UNVOTE"] = Queue()
        self.constants["QUEUE_COMMENT"] = Queue()
        self.constants["QUEUE_FOLLOW"] = Queue()
        self.constants["QUEUE_UNFOLLOW"] = Queue()

        self.constants["TO_FOLLOW_FILE"] = "tofollow.json"
        self.constants["FOLLOWED_FILE"] = "followed.json"
        self.constants["SEARCH_FILE"] = "search.json"

        self.constants["BASE_CONFIG"] = {
            "search_page_limit": 1,
            "auto_unvote": True,
            "follow_user_from_photo": True,
            "max_likes_per_day" : 100,
            "max_unlikes_per_day" : 100,
            "max_follows_per_day" : 100,
            "max_unfollows_per_day" : 10,
            "max_comments_per_day" : 50,
            "max_likes_to_like" : 250,
            "max_followers_to_follow" : 500,
            "min_followers_to_follow" : 0,
            "max_following_to_follow" : 500,
            "min_following_to_follow" : 5,
            "max_followers_to_following_ratio" : 3,
            "max_following_to_followers_ratio" : 3,
            "min_likes_to_like" : 30,
            "follow_users_from_like": False,
            "unfollow_delay" : 1800,
            "unlike_delay" : 3600
        }

        self.enviroment_variables["STATS"] = {
            "commentCounter": {},
            "voteCounter": {},
            "unvoteCounter": {},
            "followingCounter": {},
            "unfollowingCounter": {}
        }

        # self.initVote()

    # I don't need it here
    # def makeRequest(self, method, url, data = {}, headers = {}, checkStatusCode = True, proxies = None):
    #    return super(Bot, self).makeRequest(self, method, url, data = {}, headers = {}, checkStatusCode = True, proxies = None)

    def login(self):
        return super(Bot, self).login()

    def logout(self):
        return super(Bot, self).logout()

    def buildSearchParams(self):
        print "Check search params..."
        if "searchParams" in self.enviroment_variables["configValues"]:
            print "Found search params: building"
            searchParams = []
            for tag in self.enviroment_variables["configValues"]["searchParams"]["tags"]:
                sort = ""
                categories = []
                typeSearch = "fresh"

                if "sort" in self.enviroment_variables["configValues"]["searchParams"]:
                    sort = self.enviroment_variables["configValues"]["searchParams"]["sort"]

                if "type" in self.enviroment_variables["configValues"]["searchParams"]:
                    typeSearch = self.enviroment_variables["configValues"]["searchParams"]["type"]

                if "categories" in self.enviroment_variables["configValues"]["searchParams"]:
                    categories = self.enviroment_variables["configValues"]["searchParams"]["categories"]

                searchParams.append({"term": tag, "typeSearch": typeSearch, "sort": sort, "categories": categories})
        
        print "DEBUG: we have " + str(len(searchParams)) + " search criteria"

        # print "DEBUG: Append data in " + SEARCH_FILE
        # appendToFile(searchParams, SEARCH_FILE)
        return searchParams

    def search(self, term="", typeSearch="photos", sort="", categories=[], exclude_nude=True, page=1):
        searchParams = []
        if term == "" and categories == []:
            searchParams = self.buildSearchParams()
        elif term != "" or categories != []:
            searchParams.append({"term": term, "typeSearch": typeSearch, "sort": sort, "categories": categories})    
        
        if len(searchParams) > 0:
            self.initVote()
            self.initComment()
            for searchParam in searchParams:
                result = super(Bot, self).search(searchParam)
                print "Found " + str(len(result)) + " photos"
        else:
            print "No search params defined"

        return True

    def initComment(self):
        for i in range(self.constants["WORKER_THREADS"]):
            worker = Thread(target=super(Bot, self).initCommentThreads, args=())
            worker.setDaemon(True)
            worker.start()
        
        print "init comment threads"

    def initVote(self):
        for i in range(self.constants["WORKER_THREADS"]):
            worker = Thread(target=super(Bot, self).initVoteThreads, args=())
            worker.setDaemon(True)
            worker.start()

        print "Init vote threads"

    def vote(self, el):
        # vote a single photo
        # i need to know which photo is..
        return False

    def unvote(self, el):
        # unvote a single photo
        # i need to know which photo is..
        return False

    def store_queue(self):
        filenames = ["SEARCH", "VOTE", "UNVOTE", "COMMENT", "FOLLOW", "UNFOLLOW"]
        for filename in filenames:
            queueKey = "QUEUE_"+filename
            with open("backup/"+filename, mode='w') as backup:
                json.dump(self.constants[queueKey].queue, backup)
                print "Saved into backup/"+filename + " " + queueKey

        return True
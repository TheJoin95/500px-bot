# -*- coding: utf-8 -*-

import requests
import time
import json
import sys
import logging
from random import randint
from bs4 import BeautifulSoup

from search import search
from vote import *
from comment import *

class API(object):
    def __init__(self):
        self.isLoggedIn = False
        self.enviroment_variables = {}
        self.constants = {}

        # handle logging
        self.logger = logging.getLogger('[500px-bot]')
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename='500px-bot.log',
                            level=logging.INFO
                            )
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def makeRequest(self, method, url, data = {}, headers = {}, checkStatusCode = True, proxies = None):
        response = False
        try:
            response = self.enviroment_variables["userSession"].request(method, url, data = data, headers = headers, proxies = None, timeout = 5)
        except requests.exceptions.RequestException:
            self.logger.info("request timeout")
            time.sleep(5)
            pass
        if checkStatusCode and response.status_code != 200:
            self.logger.info("error on request")
            time.sleep(5)
            pass
        return response

    def initVoteThreads(self):
        vote(self, self.constants["QUEUE_VOTE"])
        self.logger.info("Initialized Vote Thread")
        return True

    def initCommentThreads(self):
        doComment(self, self.constants["QUEUE_COMMENT"])
        self.logger.info("Initialized Comment Thread")
        return True

    def initFollowThreads(self):
        doFollow(self, self.constants["QUEUE_FOLLOW"])
        self.logger.info("Initialized Follow Thread")
        return True

    def initUnFollowThreads(self):
        unFollow(self, self.constants["QUEUE_UNFOLLOW"])
        self.logger.info("Initialized Unfollow Thread")
        return True
    
    def doComment(self):
        return False
    
    # not in use right now, but maybe here i need to add in queue the photo to like
    def vote(self, el):
        return False

    # not in use right now, but maybe here i need to add in queue the photo to like
    def unvote(self, el):
        return False
    
    def search(self, searchParam={}):
        """
        search is the main function: it is processing the request and put the element in the queue
        """
        #self.initVoteThreads()
        searchResult = []
        pageLimit = self.constants["BASE_CONFIG"]["search_page_limit"]
        if "searchParams" in self.enviroment_variables["configValues"]:
            if "pageLimit" in self.enviroment_variables["configValues"]["searchParams"]:
                pageLimit = self.enviroment_variables["configValues"]["searchParams"]["pageLimit"]

        # put the request in a queue, so we can have multithread searching for multiaccount
        for page in xrange(1, pageLimit+1):
            self.logger.info("Request for " + searchParam["term"] + " type: " + searchParam["typeSearch"] + " sort: " + searchParam["sort"] + " page: " + str(page))
            tmpSearchArray = search(self, term=searchParam["term"], typeSearch=searchParam["typeSearch"], sort=searchParam["sort"], categories=searchParam["categories"], page=page)
            if len(tmpSearchArray) > 0 and searchParam["typeSearch"] in tmpSearchArray and len(tmpSearchArray[searchParam["typeSearch"]]) > 0:
                for item in tmpSearchArray[searchParam["typeSearch"]]:
                    # check if i can vote and if i can comment and i can follow
                    # need to check in config
                    # put it in a function...
                    self.constants["QUEUE_VOTE"].put(item)
                    self.constants["QUEUE_COMMENT"].put(item)
                    # self.constants["QUEUE_FOLLOW"].put(self.follow(item))
                
                searchResult = searchResult + tmpSearchArray[searchParam["typeSearch"]]
            
            time.sleep(randint(15, 35)) # I need to wait some seconds to do another search
        
        # add result in all active queue and|or in file

        return searchResult
    
    def login(self):
        """
        doLogin make a request with user and password passed in the config file or on CLI
        If the request of login will go fine, then the function return True
        Otherwise the function will return False
        """
        responseLoginPost = False
        if "paramsLogin" in self.enviroment_variables["configValues"]:
            loginPage = self.makeRequest('GET', self.constants["DOMAIN"] + '/login')
            time.sleep(3)

            loginPageHTML = BeautifulSoup(loginPage.text, 'html.parser')
            self.enviroment_variables["configValues"]['paramsLogin']['authenticity_token'] = loginPageHTML.find('meta', {'name': 'csrf-token'}).get('content')
            self.enviroment_variables["configValues"]["csrfHeaders"]['X-CSRF-Token'] = self.enviroment_variables["configValues"]['paramsLogin']['authenticity_token']

            userLogin = self.makeRequest('POST', self.constants["API_DOMAIN"] + '/session', data = self.enviroment_variables["configValues"]['paramsLogin'])
            if(userLogin.status_code == 200):
                self.logger.info('Logged in')
                userJSON = json.loads(userLogin.content)
                responseLoginPost = True
                self.enviroment_variables["configValues"]["user_data"] = userJSON["user"]

        return responseLoginPost

    def logout(self):
        """
        logout make a request of delete, for log out from our account.
        We need an authenticity_token.
        Return true or false
        """
        # need to get back, from the last request, the "authenticity_token" of logout's form

        logoutParams = {
            "_method": "delete",
            "authenticity_token": self.enviroment_variables["configValues"]["csrfHeaders"]['X-CSRF-Token']
        }

        logoutPage = self.makeRequest("POST", self.constants["DOMAIN"]+"/" + self.constants["API_ENDPOINT_LOGOUT"], data = logoutParams)
        if logoutPage.status_code == 200:
            print "Logged out"
            self.logger.info('Logged out')
        
        return (logoutPage.status_code == 200)
from random import randint
import time
import json

def checkAlreadyVoted(self, idphoto=''):    
    response = False
    page = 1

    while 1:
        votes = getLikesOfPhoto(self, idphoto=idphoto, page=page)
        if "users" in votes and len(votes["users"]) > 0:
            for vote in votes["users"]:
                if(vote["id"] == self.enviroment_variables["configValues"]["user_data"]["id"]):
                    response = True
                    break
                if self.constants["BASE_CONFIG"]["follow_user_from_photo"] == True or self.enviroment_variables["configValues"]["follow_user_from_photo"] == True:
                    self.constants["QUEUE_FOLLOW"].put({"from_vote":vote, "id": vote["id"]})
        else:
            break

        if(response == True):
            break
        else:
            page = page + 1

    self.logger.info("Is "+ str(idphoto) + " already voted: " + str(response))
    # print "checking already votes: " + str(response)
    return response

def vote(self, q):
    """https://api.500px.com/v1/photos/{idphoto}/vote?vote=1 POST"""
    
    while True:
        idphoto = ""
        response = False
        can_i_vote = (randint(1, 300) % 5)

        try:
            el = q.get()
        except q.Empty:
            self.logger.info("Queue vote is empty")
            continue
            pass
        
        # add check of configValues and increment count per day
        if (("voted" not in el or el["voted"] == False) and can_i_vote):
            idphoto = str(el['id'])
        elif ((not checkAlreadyVoted(self, el["id"])) and can_i_vote):
            idphoto = str(el['id'])
        else:
            self.logger.info("I can not vote this: " + str(el['id']))
            continue

        try:
            vote = self.enviroment_variables["userSession"].post(self.constants["API_DOMAIN"] + '/photos/' + idphoto + '/vote?vote=1', headers = self.enviroment_variables["configValues"]["csrfHeaders"])
            if vote.status_code == 200:
                # print 'Voted for ' + idphoto
                self.logger.info("Voted for " + idphoto)
                # updateStats("voteCounter") # da riattivare le statistiche ed i counter
                if self.constants["BASE_CONFIG"]["auto_unvote"] == True or self.enviroment_variables["configValues"]["auto_unvote"] == True:
                    self.constants["QUEUE_UNVOTE"].put({"idphoto":idphoto, "ttl": (time.time() + (randint(30, 120) * 10))})
                response = True
            elif vote.status_code == 404:
                self.logger.info("404 - Photo not exists")
                # print "404 - photo not exists"
            else:
                # print vote.status_code
                self.logger.info("Error while voting: " + str(vote.status_code))

            pass
        except Exception, e:
            #print "exception vote: " + str(e)
            self.logger.info("Exception while voting: " + str(e))
            pass


        q.task_done() # I need to task_done here, otherwise I will check the same entry
        time.sleep(randint(15, 45))

def unVote(self, q):
    """https://api.500px.com/v1/photos/{idphoto}/vote DELETE"""

    while True:
        response = False
        can_i_unvote = (randint(1, 300) % 5)

        try:
            el = q.get()
        except q.Empty:
            self.logger.info("Queue vote is empty")
            continue
            pass

        if can_i_unvote == False and ("ttl" not in el or el["ttl"] > time.time()):
            if self.constants["BASE_CONFIG"]["auto_unvote"] == True or self.enviroment_variables["configValues"]["auto_unvote"] == True:
                self.constants["QUEUE_UNVOTE"].put(el)
            
            continue

        try:
            vote = self.enviroment_variables["userSession"].delete(self.constants["API_DOMAIN"] + '/photos/' + str(el["idphoto"]) + '/vote', headers = self.enviroment_variables["configValues"]["csrfHeaders"])
            if vote.status_code == 200:
                self.logger.info('Unvoted for ' + el["idphoto"])
                response = True
                # updateStats("voteCounter", type="decrement") # riattivare votecounter
            elif vote.status_code == 404:
                self.logger.info("404 - photo not exists")
            else:
                self.logger.info("Status code (unvote): " + str(vote.status_code))

            pass
        except Exception, e:
            self.logger.info("exception unvote: " + str(e))
            pass

        q.task_done()
        time.sleep(randint(5, 15))

def getLikesOfPhoto(self, idphoto, page=0):
    """https://api.500px.com/v1/photos/{idphoto}/votes?include_following=true&page=2&rpp=8 GET"""
    votes = []
    try:
        votes = self.enviroment_variables["userSession"].get(self.constants["API_DOMAIN"] + '/photos/' + str(idphoto) + '/votes?include_following=true&page='+str(page)+'&rpp=8', headers = self.enviroment_variables["configValues"]["csrfHeaders"])
        if votes.status_code == 200:
            # print 'getlikes for ' + str(idphoto)
            self.logger.info("Getlike for " + str(idphoto))
            votes = json.loads(votes.text)
        elif votes.status_code == 404:
            self.logger.info("404 - Photo not exists")
            # print "404 - photo not exists"
        else:
            # print votes.status_code
            self.logger.info("error while retrieve like of photo: " + str(votes.status_code))

        pass
    except Exception, e:
        # print "exception getlikes: " + str(e)
        self.logger.info("Exception in getlikes: " + str(e))
        pass

    return votes
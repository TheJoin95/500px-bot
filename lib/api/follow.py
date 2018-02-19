from random import randint
import json
import time

def unFollow(self, q):
    """https://500px.com/{username}/unfollow POST"""
    
    while True:
        can_i_unfollow = (randint(1, 1000) % 7)

        try:
            el = q.get()
        except q.Empty:
            self.logger.info("Queue vote is empty")
            continue
            pass

        if can_i_unfollow == 0:
            try:
                unfollowResp = self.enviroment_variables["userSession"].post(self.constants["API_DOMAIN"] + '/' + username + '/unfollow', headers = self.enviroment_variables["configValues"]["csrfHeaders"])
                if unfollowResp.status_code == 200:
                    self.logger.info('Unfollowed ' + el["username"])
                    # updateStats("unfollowingCounter")
                elif unfollowResp.status_code == 404:
                    self.logger.info("404 - user not exists")
                else:
                    self.logger.info(unfollowResp.status_code)

                pass
            except Exception, e:
                self.logger.info(e)
                pass

        
        q.task_done()
        time.sleep(randint(30, 120))

def doFollow(self, q):
    """https://500px.com/{username}/follow POST"""
    
    while True:
        can_i_follow = (randint(1, 1000) % 7)

        try:
            el = q.get()
        except q.Empty:
            self.logger.info("Queue vote is empty")
            continue
            pass

        if can_i_follow == 0:
            try:
                follow = self.enviroment_variables["userSession"].post(self.constants["API_DOMAIN"] + '/' + el["username"] + '/follow', headers = self.enviroment_variables["configValues"]["csrfHeaders"])
                if follow.status_code == 200:
                    print "Following " + el["username"]
                    # updateStats("followingCounter")
                    # appendToFile(username, FOLLOWED_FILE)
                elif follow.status_code == 404:
                    self.logger.info(el["username"] + " not exists")
                else:
                    self.logger.info(follow.status_code)

                pass
            except Exception, e:
                self.logger.info(e)
                pass


        q.task_done()
        time.sleep(randint(30, 120))

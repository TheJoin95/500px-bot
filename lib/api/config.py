import Queue

DOMAIN = "https://500px.com"
API_DOMAIN = "https://api.500px.com/v1"
API_ENDPOINT_UNFOLLOW = "unfollow"
API_ENDPOINT_LOGOUT = "logout"

WORKER_THREADS = 3 # definire max worker per queue
MAX_WORKER_SEARCH = 10
QUEUE_SEARCH = Queue()
QUEUE_VOTE = Queue()
QUEUE_UNVOTE = Queue()
QUEUE_COMMENT = Queue()
QUEUE_FOLLOW = Queue()
QUEUE_UNFOLLOW = Queue()

TO_FOLLOW_FILE = "tofollow.json"
FOLLOWED_FILE = "followed.json"
SEARCH_FILE = "search.json"

BASE_CONFIG = {
    "search_page_limit": 2,
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
    "follow_users_from_like": false,
    "unfollow_delay" : 1800,
    "unlike_delay" : 3600
}

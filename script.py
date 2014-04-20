from pprint import pprint as pp
import ConfigParser
import random
from twitter import Twitter, OAuth

config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret'))

t = Twitter(auth=oauth)

def get_mentioners():
    ## Check mentions
    mentions = t.statuses.mentions_timeline(count=200)
    ## Get users
    users = set([(mention['user']['screen_name'],mention['user']['id'])
                 for mention in mentions])
    return users

def select(users):
    while len(users) > 0:
        ## pick a random mentioner
        ruser = random.sample(users,1)[0]
        users.remove(ruser)

        ## test to see if they follow
        friendship = t.friendships.show(source_screen_name='sbenthall',target_id=ruser[1])

        if friendship['relationship']['source']['followed_by']:
            return ruser

    return None

def get_last_tweet(user):
    return t.statuses.user_timeline(screen_name=user[0])[0]

def tweetserve():
    mentioners = get_mentioners()

    while len(mentioners) > 0:
        selected = select(mentioners)

        pp(selected)

        last = get_last_tweet(selected)

        pp(last['text'])

        try:
            result = t.statuses.retweet(id=last['id'])
            return result
        except:
            pass

    #if none could be retweeted, do nothing
    pp('Nothing could be retweeted')
    return None

tweetserve()

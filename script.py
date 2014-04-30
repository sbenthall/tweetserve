from pprint import pprint as pp
from funcs import *
import time
import random
import ConfigParser

config= ConfigParser.ConfigParser()
config.read('config.cfg')

PERIOD = int(config.get('Run','period'))

## currently set to make it so we don't hit window
## rate limits on friendship/show
## should be able to increase to 200 when using
## friendship/lookup
LIMIT = config.get('Run','limit')

def wait(period):
    window_in_seconds = period * 60
    seconds = random.randint(0,window_in_seconds)
    pp("Waiting %d minutes" % (float(seconds) / 60) )
    time.sleep(seconds)

def tweetserve():
    # get the latest mentioners
    mentioners = get_mentioners(LIMIT)
    pp("# mentioners: %d" % len(mentioners))

    # filter out those whose tweets are protected
    mentioners = [m for m in mentioners if not m['protected']]
    pp("# unprotected mentioners: %d" % len(mentioners))

    ids = list(set([m['id'] for m in mentioners]))
    pp("# unique ids: %d" % len(ids))

    friendships = lookup_friendships(ids)

    #filter out people that don't follow
    friendships = [f for f
                   in friendships
                   if 'followed_by' in f['connections']]
    pp("# following mentioners: %d" % len(friendships))

    selected = random.sample(friendships,1)[0]
    pp("Selected friend: %s / @%s" % (selected['name'],selected['screen_name']))
    pp("Connections: %s" % (",".join(selected['connections'])))

    sn = selected['screen_name']
    #selects last 20 tweets by default but could have this be a setting
    tweets = t.statuses.user_timeline(screen_name=sn)

    if 'following' not in selected['connections']:
        new_friend = t.friendships.create(screen_name=sn)
        pp("Created new friendship")

    rt = None

    while rt is None and len(tweets) > 0:
        lt = tweets.pop(0)
        try:
            rt = t.statuses.retweet(id=lt['id'])
            pp("RT: @%s: %s" % (lt['user']['screen_name'],lt['text']))
        except:
            pp("Unable to RT tweet: @%s: %s" % (lt['user']['screen_name'],lt['text']))
            pass

wait(PERIOD)
tweetserve()

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

    try:
        sn = selected['screen_name']
        lt = get_last_tweet(sn)
        rt = t.statuses.retweet(id=lt['id'])
        pp("RT: %s" % lt['text'])

        if 'following' not in selected['connections']:
            new_friend = t.friendships.create(screen_name=sn)
            pp("Created new friendship")
    except:
        '''
        e.g.:
        twitter.api.TwitterHTTPError: Twitter sent status 403 for URL: 1.1/statuses/retweet/458044608862121984.json using parameters: (oauth_consumer_key=xPWeJ3r8hEjI33spI1ZN6B1P0&oauth_nonce=9177998659638958997&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1398041579&oauth_token=2300627557-lhe1sbDBE6xFrLowAb40QDYR4D0BLvCDkKcwQfp&oauth_version=1.0&oauth_signature=M8r%2BQ71GDCMs%2FkrNbxmeyAsnv0o%3D)
        details: {"errors":"sharing is not permissible for this status (Share validations failed)"

        '''
        pass

wait(PERIOD)
tweetserve()

import ConfigParser
from twitter import Twitter, OAuth


config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret'))

t = Twitter(auth=oauth)


def get_mentioners(limit):
    ## Check mentions
    mentions = t.statuses.mentions_timeline(count=limit)
    ## Get users
    users = [mention['user'] for mention in mentions]
    return users
                  
def lookup_friendships(ids):
    friendships = []
    
    for user_slice in [ids[x:x+100]
                       for x
                       in xrange(0,len(ids),100)]:
        query = ",".join([str(x) for x in ids])

        result = t.friendships.lookup(user_id=query,_method="GET")
        friendships.extend(result)

    return friendships

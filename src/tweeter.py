import tweepy


class Tweeter(object):
    def __init__(self):
        self.consumer_key = 'TKTcvwU9Fy5wFjXDWxdagZQ5J'
        self.consumer_secret = 'm5RJMJqV6GJlDxY3fg0R1sp7sYwH7MGQSU8ZBD9RU1aYgty5bC'
        self.key = '1401846892342939649-i4dHvRw9hSdWaE4RMOh4oyUIv2XVqg'
        self.secret = 'kEkcJ6YgSyA49rLy4TnNtERtcPcbVyfomOUYApAZkHA1G'

    def tweet_tautology(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)

        api = tweepy.API(auth)

        try:
            api.verify_credentials()
            print('verification ok')
        except:
            print('Issue during verification')

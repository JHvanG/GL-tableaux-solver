import tweepy
import keys


class Tweeter(object):
    def __init__(self):
        self.consumer_key = keys.consumer_key
        self.consumer_secret = keys.consumer_secret
        self.key = keys.access_token
        self.secret = keys.access_secret

    def tweet_tautology(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)

        api = tweepy.API(auth)

        #api.update_status("Hello World!")

        api.update_status("Hello World!")

        #try:
        #    api.verify_credentials()
        #    print('verification ok')
        #except:
        #    print('Issue during verification')

if __name__ == "__main__":
    tweeter = Tweeter()
    tweeter.tweet_tautology()